#   coding = utf-8
#   HUAWEI STORE GO 项目Github地址：https://github.com/XYZliang/HUAWEI-STORE-GO
#   本python脚本仅供大家学习交流，严禁严禁用于商业用途，不得利用本项目进行任何形式的盈利活动，请在24小时内删除。
#   如果本项目对你有所帮助，麻烦项目给个星星鼓励一下哦

from selenium import webdriver
import time
from threading import Thread

ACCOUNTS = {
    "华为账户账号/电话/邮箱": "账户密码"
}

chrome_driver = "/usr/local/bin/chromedriver"   # Mac示例
#chrome_driver = "C:\Google\ChromeApplication\chrome.exe"   # Windows示例

# 测试Nova 8
BUY_URL = 'https://www.vmall.com/product/10086232069466.html'
# 开始自动刷新等待抢购按钮出现的时间点,建议提前10-30s，并提前2-5分钟启动python脚本，确保登陆成功，进入页面。
BEGIN_GO = '2021-01-21 10:07:50'
#是否启动自动选手机参数。1为开启，0为关闭。当不启用时，无需填写下面的参数，此时抢购会默认网页上的默(第一个颜色、版本、套餐)。若不需要请关闭此选项能加快速度。
AUTO_SELECT=1
#是否启动自动选手机颜色
AUTO_COLOR=1
#是否启动自动选手机版本
AUTO_EDITION=1
#是否启动自动选手机套餐
AUTO_COMBO=1
#颜色，仅当AUTO_SELECT=1和AUTO_COLOR=1时才需要写
COLOR='8号色'
#版本，仅当AUTO_SELECT=1和AUTO_EDITION=1时才需要写
EDITION='5G全网通 8GB+256GB'
#套餐，仅当AUTO_SELECT=1和AUTO_COMBO=1时才需要写
COMBO='官方标配'

# 登录url,一般无需改动
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL,一般无需改动
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/'
# 登陆信任 0表示不信任，1表示信任。一般无需改动。若信任，当您下次登录时，系统将不会要求您提供验证码。对于HUAWEI STORE普通版脚本，每次运行脚本即创建一个新Chrome，信任意义不大，默认为0，建议设置为0
TRUST = 0

# 进到购买页面后提交订单


def submitOrder(driver, user):
    time.sleep(1)
    while BUY_URL == driver.current_url:
        print(user + ':当前页面还在商品详情！！！')
        time.sleep(3)

    while True:
        try:
            submitOrder = driver.find_element_by_link_text('提交订单')
            submitOrder.click()
            print(user + ':成功提交订单')
            break
        except:
            print(user + ':提交不了订单！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
            time.sleep(1)  # 到了订单提交页面提交不了订单一直等待
            pass
    while True:
        print(user + ':进入睡眠3000s')
        time.sleep(3000)
        pass


# 排队中
def onQueue(driver, user):
    time.sleep(1)
    nowUrl = driver.current_url
    print(user + '开始排队：' + BEGIN_GO)
    while True:
        errorbutton = driver.find_element_by_id("boxCloseBtn")
        if errorbutton.get_attribute('style') == 'display: none;':
            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime())+user + "抢购失败，再试一次")
            goToBuy(driver, user)
        else:
            if nowUrl != driver.current_url and driver.current_url != BUY_URL:
                print(user + ':成功！排队页面跳转了!!!!!!!!!!!!!!')
                submitOrder(driver, user)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime())+user + ':排队中')
                time.sleep(0.2)  # 排队中

# 选择手机规格


def select(driver, user):
    if AUTO_COLOR == 1:
        try:
            color = driver.find_element_by_link_text(COLOR)
            color.click()
            print(user+COLOR + '选择成功！')
        except:
            time.sleep(1)
            try:
                color = driver.find_element_by_link_text(COLOR)
                color.click()
                print(user+COLOR + '选择成功！')
            except:
                print(user+'颜色选择错误！请手动选择！')
    else:
        print(user+'无需选择颜色')

    if AUTO_EDITION == 1:
        try:
            edition = driver.find_element_by_link_text(EDITION)
            edition.click()
            print(user+EDITION + '选择成功！')
        except:
            time.sleep(1)
            try:
                edition = driver.find_element_by_link_text(EDITION)
                edition.click()
                print(user+EDITION + '选择成功！')
            except:
                print(user+'版本选择错误！请手动选择！')
    else:
        print(user+'无需选择版本')

    if AUTO_COMBO == 1:
        try:
            combo = driver.find_element_by_link_text(COMBO)
            combo.click()
            print(user+COMBO + '选择成功！')
        except:
            time.sleep(1)
            try:
                combo = driver.find_element_by_link_text(COMBO)
                combo.click()
                print(user+COMBO + '选择成功！')
            except:
                print(user+'套餐选择错误！请手动选择！')
    else:
        print(user+'无需选择套餐')

# 登录成功去到购买页面


def goToBuy(driver, user):
    autoSelect = AUTO_SELECT
    driver.get(BUY_URL)
    time.sleep(0.5)
    if BUY_URL != driver.current_url:
        driver.get(BUY_URL)
    print(user + '打开购买页面')
    time.sleep(0.5)
    # 转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # 再次登陆
    try:
        denglu1 = driver.find_element_by_id("top-index-loginUrl")
        denglu1.click()
        time.sleep(0.5)
    except:
        print(user + '已经登陆')
    # 结束标志位
    over = False
    time.sleep(0.5)
    if(autoSelect == 1):
        select(driver, user)
    else:
        print(user+'跳过选择配置')
    isRemind = 0
    while True:
        if isRemind == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime()) + user + '准备完毕，开始等待')
            isRemind = 1
        if time.time() >= timestamp:  # 到了抢购时间
            text = driver.find_elements_by_xpath(
                '//*[@id="pro-operation"]/a')[0].text
            if text == '已售完':
                over = True
                break
            if text == '立即申购':
                buyButton = driver.find_element_by_link_text('立即申购')
                if buyButton.get_attribute('class') != 'product-button02 disabled':
                    print(time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime()) + user + '可以开始申购，立即申购')
                    buyButton.click()
                    break
                else:
                    try:
                        textnext = driver.find_elements_by_xpath(
                            '//div[@id="pro-operation-countdown"]/p')[0].text
                        if isRemind != 2:
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                  user + '准备开始下一轮' + textnext.replace('开售:', '') + '的抢购')
                    except:
                        if isRemind != 2:
                            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime()) + user + '准备开始下一轮的抢购')
                            isRemind != 2
            else:
                over = True
                break
        elif time.time() < timestamp-15:
            if isRemind == 1:
                isRemind = 2
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                      user + '未到脚本开启时间，请选择好抢购的颜色、版本、套餐等(若已经配置则忽略)，将在设定的脚本启动时间前15秒启动')
            else:
                print('-', end="")
            time.sleep(0.99)
        else:
            if isRemind == 1 or isRemind == 2:
                if isRemind == 2:
                    print("")
                isRemind = 3
                print(time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime()) + user + '即将开始抢购，程序启动')
                time.sleep(0.05)

    if over:
        print(user+"很遗憾，"+time.strftime("%H:%M:%S",
                                        time.localtime())+"抢购结束,程序将在60s后退出")
        time.sleep(60)
        driver.quit()
        exit()
    else:
        onQueue(driver, user)

# 信任浏览器(driver)


def trustdriver(driver, user):
    try:
        if TRUST == 0:
            try:
                trust = driver.find_element_by_xpath(
                    '//div[@ht="click_dialog_leftbtn"]')
                trust.click()
            except:
                print(user+'不信任出错，请自行点击不信任')
        if TRUST == 1:
            try:
                trust = driver.find_element_by_xpath(
                    '//div[@ht="click_dialog_rightbtn"]')
                trust.click()
            except:
                print(user + '信任出错，请自行点击信任')
    except:
        return

# 发送验证码


def sendcode(driver, user):
    try:
        isGetVerification = driver.find_element_by_xpath(
            '//div[@ht="click_authentication_getAuthcode"]')
        number = driver.find_element_by_xpath('//div[@id="accountDiv"]')
    except:
        time.sleep(0.2)
    if isGetVerification.text == '获取验证码':
        isGetVerification.click()
        if number is None:
            print(user + '验证码已经发送')
        else:
            print(user+'验证码已经发送至'+number.text)
        try:
            inputdiv = driver.find_element_by_xpath(
                '//input[@ht="input_authentication_authcode"]')
            inputdiv.click()
            # 自动点击输入框
        except:
            time.sleep(0.1)
    time.sleep(0.1)

# 登录商城,登陆成功后至商城首页然后跳转至抢购页面


def loginMall(user, pwd):
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(LOGIN_URL)
    try:
        time.sleep(3)  # 等待页面加载完成
        account = driver.find_element_by_xpath(
            '//input[@ht="input_pwdlogin_account"]')
        account.send_keys(user)
        password = driver.find_element_by_xpath(
            '//input[@ht="input_pwdlogin_pwd"]')
        password.send_keys(pwd)
        denglu = driver.find_element_by_xpath(
            '//div[@ht="click_pwdlogin_submitLogin"]')
        denglu.click()
        print(user + '成功输入了账号密码，尝试登陆.')
    except:
        print(user + '账号密码不能输入,请手动输入并登陆！')
    isRemind = 0
    islogin = 0
    while True:
        time.sleep(0.5)
        if LOGIN_SUCCESS_CONFIRM == driver.current_url:  # 页面跳转登陆成功
            print(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime()) + user + '登录成功！！')
            break
        else:  # 没有登陆成功
            if isRemind == 0:
                print(user + '请手动完成认证并登陆！')
                isRemind = 1
            try:  # 判断是否在获取验证码界面
                isGetVerification = driver.find_element_by_xpath(
                    '//div[@class="hwid-dialog-header paddingBottom18"]/div')
                if isGetVerification.text == '身份验证':
                    sendcode(driver, user)
                    islogin = 1
            except:
                time.sleep(0.05)
            if islogin == 1:
                try:  # 判断是否在信任浏览器界面
                    isGetVerification = driver.find_element_by_xpath(
                        '//div[@class="hwid-dialog-header paddingBottom40"]/div')
                    if '是否信任此浏览器' in isGetVerification.text:
                        islogin = 2
                        trustdriver(driver, user)
                except:
                    time.sleep(0.05)
            if islogin == 0 or islogin == 1:
                try:
                    error = driver.find_element_by_xpath(
                        '//div[@class="marginTB8 hwid-input-msg-error"]').text
                    print(error)
                except:
                    time.sleep(0.1)
                if '图形验证码' in error:
                    try:
                        denglu.click()
                    except:
                        time.sleep(0.1)
                elif '较为频繁' in error:
                    print('验证码获取频繁，请一小时后再试，或者使用HUAWEI STORE GO DEV版信任浏览器')
                    print('60s后程序退出')
                    time.sleep(60)
                    exit()
    goToBuy(driver, user)


if __name__ == "__main__":
    # 账号密码
    data = ACCOUNTS
    # 构建线程
    threads = []
    for account, pwd in data.items():
        t = Thread(target=loginMall, args=(account, pwd,))
        threads.append(t)
        # 启动所有线程
    for thr in threads:
        time.sleep(1)
        thr.start()
