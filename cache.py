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
      - the license, being applied to the files, if present;

    This defines how the emoji looks, and makes it such that a change in either
    the source or the manifest palette will not reuse the file in cache.
    """

    cache_dir = None

    # Formats for which a non-licensed version should never be cached
    skip_export_cache_formats = set(('svg'))

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
    def generate_cache_key_from_parts(key_parts):
        """
        Calculate a unique hash from the given key parts, building the data to
        feed to the algorithm from the repr() encoded as UTF-8.
        This should be stable as long as the inputs are the same, as we're
        using data structures with an order guarantee.
        """
        raw_key = bytes(repr(key_parts), 'utf-8')
        return hashlib.sha256(raw_key).hexdigest()

    @staticmethod
    def get_cache_keys(emoji, manifest, emoji_src, license_enabled):
        """
        Get the cache keys for a given emoji, base and for each license format
        if license_enabled is set.

        This needs to take into account multiple parts:
            - SVG source file: Allows tracking changes to the source
            - Colour modifiers, if applicable: Tracks changes in the manifest
            - License contents, only for each of the license formats
        """
        if 'cache_keys' in emoji:
            return emoji['cache_keys']

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
        key_parts_base = (
            ('src_hash', src_hash),
            ('colors', colors),
        )

        key_base = Cache.generate_cache_key_from_parts(key_parts_base)
        key_licenses = None

        if license_enabled:
            key_licenses = {}
            for license in manifest.license:
                # Obtain the license to add to the key parts
                license_content = bytes(repr(manifest.license[license]),
                                        'utf-8')
                key_parts = key_parts_base + (('license', license_content), )

                key = Cache.generate_cache_key_from_parts(key_parts)
                key_licenses[license] = key

        keys = {
            'base': key_base,
            'licenses': key_licenses,
        }

        return keys

    def build_emoji_cache_path(self, emoji, f, license_enabled):
        """
        Build the full path to the cache emoji file (regardless of existence).
        If `license_enabled` is `True` the path for the given format with
        license is built and returned.
        This requires the 'cache_keys' field of the emoji object that is passed
        to be present.
        If `license_enabled` is `True`, then the license type for the given
        format is used to build the path; if the format `f` does not support a
        license `None` is returned instead.
        """
        if 'cache_keys' not in emoji or 'base' not in emoji['cache_keys']:
            raise RuntimeError("Emoji '{}' does not have a cache key "
                               "set!".format(emoji['short']))

        cache_key = None

        if not license_enabled and f in self.skip_export_cache_formats:
            return None

        if license_enabled:
            if 'licenses' not in emoji['cache_keys']:
                raise RuntimeError(f"Emoji '{emoji['short']}' does not have a "
                                   "cache key set for licenses.")

            license_type = util.get_license_type_for_format(f)
            if license_type:
                if license_type in emoji['cache_keys']['licenses']:
                    cache_key = emoji['cache_keys']['licenses'][license_type]
                else:
                    raise RuntimeError(f"License type '{license_type}' cache "
                                       f"key not present for emoji "
                                       f"'{emoji['short']}'.")
        else:
            cache_key = emoji['cache_keys']['base']

        if cache_key:
            dir_path = self.build_cache_dir_by_format(f)
            return os.path.join(dir_path, cache_key)
        else:
            return None

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

    def get_cache(self, emoji, f, license_enabled):
        """
        Get the path to an existing emoji in a given format `f` that is in
        cache, or `None` if the cache file does not exist.
        If `license_enabled` is `False`, the cache file for a non-licensed
        export of the format `f` is looked up.
        If `license_enabled` is `True`, the cache file for a licensed export of
        the format `f` is looked up; if `f` does not support a license, `None`
        is returned.
        """
        cache_file = self.build_emoji_cache_path(emoji, f, license_enabled)
        if cache_file and os.path.exists(cache_file):
            return cache_file

        return None

    def save_to_cache(self, emoji, f, export_path, license_enabled):
        """
        Copy an exported path to the cache directory.
        If `license_enabled` is `False`, the `export_path` will be copied to a
        cache key for a base export of the format.
        If `license_enabled` is `True`, the `export_path` will be copied to a
        cache key for a licensed form of the format `f`; if the format `f` does
        not support a license but `license_enabled` is set, `False` is
        returned.
        """
        if not os.path.exists(export_path):
            raise RuntimeError("Could not find exported emoji '{}' at "
                               "'{}'".format(emoji['short'], export_path))

        cache_file = self.build_emoji_cache_path(emoji, f, license_enabled)

        if cache_file is None:
            return False

        try:
            shutil.copy(export_path, cache_file)
        except OSError as exc:
            raise RuntimeError("Unable to save '{}' to cache ('{}'): "
                               "{}.".format(emoji['short'], cache_file,
                                            str(exc)))

        return True

    def load_from_cache(self, emoji, f, export_path, license_enabled):
        """
        Copy an emoji from cache to its final path, `export_path`.
        If `license_enabled` is `False`, the cache for a non-licensed format
        `f` is looked up, and copied if it exists.
        If `license_enabled` is `True`, the cache for a licensed format `f` is
        looked up and copied if it exists; if `f` does not support a license,
        `False` is returned.
        """
        if not self.cache_dir:
            return False

        cache_file = self.get_cache(emoji, f, license_enabled)
        if not cache_file:
            return False

        try:
            shutil.copy(cache_file, export_path)
        except OSError as exc:
            raise RuntimeError("Unable to retrieve '{}' from cache ('{}'): "
                               "{}".format(emoji['short'], cache_file,
                                           str(exc)))
        return True

    @classmethod
    def filter_cacheable_formats(cls, fs, license_enabled):
        """
        Obtain the formats from `fs` that are cacheable given the status of the
        license.
        """
        cacheable_fs = fs

        if not license_enabled:  # Exports
            cacheable_fs = tuple(set(fs) - cls.skip_export_cache_formats)

        return cacheable_fs
