from urllib import robotparser


robot_parser = robotparser.RobotFileParser()


def prepare(robots_txt_url):
    robot_parser.set_url(robots_txt_url)
    robot_parser.read()
def is_allowed(target_url, user_agent='*'):
    return robot_parser.can_fetch(user_agent, target_url)

if __name__ == '__main__':
    prepare('https://shop.gwl.eu/robots.txt')

print(is_allowed("https://shop.gwl.eu/LiFePO4-Single-Cells/", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"))
# print(is_allowed('http://hajba.hu/category/softwaredevelopment/java-software-development/', 'my-agent'))
# print(is_allowed('http://hajba.hu/category/softwaredevelopment/java-software-development/', 'googlebot'))
