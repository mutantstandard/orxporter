import collections
import hashlib
import os
import shutil

import svg
import util


class Cache:
    """
    Implements a cache system for emoji.

    This cache is implemented based on a cache directory where files are placed
    in directories by the format they were exported to; the individual cache
    files are named by their key, which is generated from:
      - the source file of the emoji;
      - the colour modifiers applied to the emoji;

    This defines how the emoji looks, and makes it such that a change in either
    the source or the manifest palette will not reuse the file in cache.
    """

    cache_dir = None

    def __init__(self, cache_dir):
        """
        Initiate an export cache instance. Requires a directory path (which may
        or may not exist already) to function.
        """
        if not isinstance(cache_dir, str):
            raise ValueError("Cache dir must be a string path")

        self.cache_dir = cache_dir
        self.initiate_cache_dir()

    def initiate_cache_dir(self):
        """Make the cache directory if it does not exist already."""
        if not os.path.exists(self.cache_dir):
            try:
                os.mkdir(self.cache_dir)
            except OSError as exc:
                raise RuntimeError("Cannot create cache directory "
                                   "'{}'".format(self.cache_dir)) from exc
        elif not os.path.isdir(self.cache_dir):
            raise RuntimeError("Cache path '{}' exists but is not a "
                               "directory".format(self.cache_dir))

        return True

    @staticmethod
    def get_cache_key(emoji, manifest, emoji_src):
        """
        Get the cache key for a given emoji.

        This needs to take into account multiple parts:
            - SVG source file: Allows tracking changes to the source
            - Colour modifiers, if applicable: Tracks changes in the manifest
        """
        if 'cache_key' in emoji:
            return emoji['cache_key']

        src = emoji_src
        if isinstance(src, collections.abc.ByteString):
            src = bytes(src, 'utf-8')
        src_hash = hashlib.sha256(bytes(emoji_src, 'utf-8')).digest()

        # Find which variable colours are in this emoji
        colors = None
        if 'color' in emoji:
            pal_src, pal_dst = util.get_color_palettes(emoji, manifest)
            colors = []

            changed = svg.translated_colors(emoji_src, pal_src, pal_dst)
            colors = sorted(changed.items())

        # Collect the parts
        key_parts = (
            ('src_hash', src_hash),
            ('colors', colors),
        )

        # Calculate a unique hash from the parts, building the data to feed
        # to the algorithm from the repr() encoded as UTF-8.
        # This should be stable as long as the inputs are the same, as we're
        # using data structures with an order guarantee.
        raw_key = bytes(repr(key_parts), 'utf-8')
        key = hashlib.sha256(raw_key).hexdigest()

        return key

    def build_emoji_cache_path(self, emoji, f):
        """
        Build the full path to the cache emoji file (regardless of presence).
        This requires the 'cache_key' field of the emoji object that is passed
        to be present.
        """
        if 'cache_key' not in emoji:
            raise RuntimeError("Emoji '{}' does not have a cache key "
                               "set!".format(emoji['short']))
        dir_path = self.build_cache_dir_by_format(f)
        return os.path.join(dir_path, emoji['cache_key'])

    def build_cache_dir_by_format(self, f):
        """
        Checks if the build cache directory for the given format exists,
        attempting to create it if it doesn't, and returns its path.
        """
        if not self.cache_dir:
            raise RuntimeError("cache dir not set")

        dir_path = os.path.join(self.cache_dir, f)
        if os.path.isdir(dir_path):
            # Return immediately if it exists
            return dir_path

        if os.path.exists(dir_path):  # Exists but is not directory
            raise RuntimeError("cache path '{}' exists, but it is not a "
                               "directory".format(dir_path))

        # Create directory
        try:
            os.mkdir(dir_path)
        except OSError as exc:
            raise RuntimeError("Cannot create build cache directory "
                               "'{}'".format(dir_path)) from exc

        return dir_path

    def get_cache(self, emoji, f):
        """
        Get the path to an existing emoji in a given format f that is in cache.
        """
        cache_file = self.build_emoji_cache_path(emoji, f)
        if os.path.exists(cache_file):
            return cache_file

        return False

    def save_to_cache(self, emoji, f, export_path):
        """Copy an exported path to the cache directory."""
        if not os.path.exists(export_path):
            raise RuntimeError("Could not find exported emoji '{}' at "
                               "'{}'".format(emoji['short'], export_path))

        cache_file = self.build_emoji_cache_path(emoji, f)

        try:
            shutil.copy(export_path, cache_file)
        except OSError as exc:
            raise RuntimeError("Unable to save '{}' to cache ('{}'): "
                               "{}.".format(emoji['short'], cache_file,
                                            str(exc)))

        return True

    def load_from_cache(self, emoji, f, export_path):
        """Copy an emoji from cache to its final path."""
        if not self.cache_dir:
            return False

        cache_file = self.get_cache(emoji, f)
        if not cache_file:
            return False

        try:
            shutil.copy(cache_file, export_path)
        except OSError as exc:
            raise RuntimeError("Unable to retrieve '{}' from cache ('{}'): "
                               "{}".format(emoji['short'], cache_file,
                                           str(exc)))
        return True
