import re

def ctrans(svg, pfrom, pto):
    res = svg
    for centry, ccol in pfrom.items():
        cr = ccol + ';'
        cro = pto.get(centry)
        if not cro:
            continue
        cro += ';'
        res = re.sub(cr, cro, res, flags=re.IGNORECASE)
        if (cr[1], cr[3], cr[5]) == (cr[2], cr[4], cr[6]):
            cr = cr[0] + cr[1] + cr[3] + cr[5] + ';'
            res = re.sub(cr, cro, res, flags=re.IGNORECASE)
    return res

def add_license(svg, license_data):
    svgidx = svg.index('<svg')
    insidx = svg.index('>', svgidx) + 1
    metastr = '\n<metadata>\n' + license_data + '</metadata>\n'
    return svg[:insidx] + metastr + svg[insidx:]

def get_viewbox_size(svg):
    try:
        x1, y1, x2, y2 = list(map(
            int, svg[svg.index('viewBox'):].split('"', 2)[1].split()))
        return x2 - x1, y2 - y1
    except Exception:
        raise ValueError('Could not detect image size')
