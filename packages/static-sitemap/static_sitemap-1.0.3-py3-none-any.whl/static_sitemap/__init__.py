"""static sitemap generator"""

from sys import argv
from re import findall
from urllib.parse import urlparse
from datetime import datetime
from requests import get

NEWS = 'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"'
XHTML = ' xmlns:xhtml="http://www.w3.org/1999/xhtml"'
IMAGE = 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
VIDEO = 'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"'

in_domain = []
ext = []
mail = []
globalVar = {}


def disp(text, end=""):
    """display text"""
    if not globalVar["quiet"]:
        if end == "\n":
            print(text)
        else:
            print(text, end="")


def parse_args():
    """parse args"""
    globalVar["verbose"] = True if "--verbose" in argv else False
    globalVar["quiet"] = True if "--quiet" in argv else False
    globalVar["sitemap"] = True if "--sitemap" in argv else False
    globalVar["rmError"] = True if "--rmError" in argv else False
    globalVar["css"] = False if "--css" in argv else True
    globalVar["json"] = False if "--json" in argv else True
    globalVar["html"] = True if "--html" in argv else False


def image(uri):
    """check if image"""
    img_ext = ["png", "jpg", "ico", "gif", "jpeg", "svg"]
    for one_ext in img_ext:
        if uri.endswith(one_ext):
            return True
    return False


def explorer(url, domain_name):
    """explore url"""
    temp_url = urlparse(url).geturl()
    try:
        response = get(temp_url, timeout=5, allow_redirects=True)
    except Exception as exception:
        disp(type(exception).__name__, "\n")
        disp(exception.__class__.__name__, "\n")
        disp(exception.__class__.__qualname__, "\n")
        return False
    web_content = response.text.strip()
    if globalVar["html"]:
        disp(web_content, "\n")
    variable = findall('href="[^"]*"', web_content)
    without_last = "/".join(response.url.split("/")[:-1])
    global_domain = urlparse(url).scheme + "://" + urlparse(url).netloc
    for one_link in variable:
        one_link = one_link.replace("href=", "")
        one_link = one_link.replace(one_link[0], "")
        # sort
        if one_link.startswith("mailto:"):
            mail.append(one_link.replace("mailto:", ""))
        elif one_link.startswith("#"):
            continue
        elif one_link.startswith("?"):
            one_link = response.url.split("?")[0] + one_link
        elif one_link.startswith("./"):
            if response.url.endswith("/"):
                one_link = response.url + one_link[2:]
            else:
                one_link = without_last + one_link[1:]
        elif one_link.startswith("//"):
            one_link = one_link.replace("//", "http://")
        elif one_link.startswith("/"):
            one_link = global_domain + one_link

        if one_link.startswith(domain_name):
            if one_link not in in_domain:
                in_domain.append(one_link)
        elif one_link not in ext:
            ext.append(one_link)


def main():
    """global main function"""
    if len(argv) <= 1:
        disp("No arguments were given")
        exit(1)
    else:
        base_url = argv[1]
    parse_args()
    domain_name = base_url.split("/")
    while len(domain_name) > 3:
        domain_name.pop()
    domain_name = "/".join(domain_name)
    domain_name += "/"
    try:
        in_domain.append(base_url)
        for one_link in in_domain:
            disp("Exploring " + one_link, "\n")
            check_file = True
            if image(one_link):
                check_file = False
            elif one_link.endswith("css"):
                if globalVar["css"]:
                    check_file = True
                else:
                    check_file = False
            elif one_link.endswith("json"):
                if globalVar["json"]:
                    check_file = True
                else:
                    check_file = False
            if check_file:
                rest = explorer(one_link, domain_name)
                if rest is False and globalVar["rmError"]:
                    in_domain.remove(one_link)
    except KeyboardInterrupt:
        pass
    except Exception as _exception:
        pass

    if not globalVar["quiet"]:
        disp("Finished Exploring", "\n")

    if globalVar["sitemap"]:
        string_to_add = ""
        string_to_add += '<?xml version="1.0" encoding="UTF-8"?>' + "\n"
        string_to_add += (
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" {NEWS} {XHTML} {IMAGE} {VIDEO}>'
            + "\n"
        )
        for one_link in in_domain:
            string_to_add += "    <url>\n"
            string_to_add += f"{' '*8}<loc>{one_link}</loc>\n"
            string_to_add += f"{' '*8}<changefreq>weekly</changefreq>\n"
            string_to_add += f"{' '*8}<priority>0.5</priority>\n"
            string_to_add += "    </url>\n"
        string_to_add += "</urlset>"
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(string_to_add)

    disp(">>> Internal : ", "")
    disp(len(in_domain), "\n")
    if globalVar["verbose"]:
        for one_link in in_domain:
            disp(one_link, "\n")

    disp(">>> External : ", "")
    disp(len(ext), "\n")
    if globalVar["verbose"]:
        for one_link in ext:
            disp(one_link, "\n")

    disp(">>> Mails : ", "")
    disp(len(mail), "\n")
    if globalVar["verbose"]:
        for one_link in mail:
            disp(one_link, "\n")


if __name__ == "__main__":
    parse_args()
    main()
