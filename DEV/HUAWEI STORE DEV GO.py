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
personalDataPath= "/Users/zhangliang/Downloads/BUY-HW-master/Default"   #Chrome的个人资料路径示例

# 测试Nova 8
BUY_URL = 'https://www.vmall.com/product/10086232069466.html'
# 开始自动刷新等待抢购按钮出现的时间点,建议提前10-30s，并提前2-5分钟启动python脚本，确保登陆成功，进入页面。
BEGIN_GO = '2021-01-18 10:07:50'
#是否启动自动选手机参数。1为开启，0为关闭。当不启用时，无需填写下面的参数，此时抢购会默认网页上的默(第一个颜色、版本、套餐)。若不需要请关闭此选项能加快速度。
AUTO_SELECT=1
#是否启动自动选手机颜色
AUTO_COLOR=1
#是否启动自动选手机版本
AUTO_EDITION=1
#是否启动自动选手机套餐
AUTO_COMBO=0}
#颜色，仅当AUTO_SELECT=1和AUTO_COLOR=1时才需要写
COLOR='8号色'
#版本，仅当AUTO_SELECT=1和AUTO_EDITION=1时才需要写
EDITION='5G全网通 8GB+256GB'
#套餐，仅当AUTO_SELECT=1和AUTO_COMBO=1时才需要写
COMBO=''

# 登录url,一般无需改动
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL,一般无需改动
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/'
# 登陆信任 0表示不信任，1表示信任。一般无需改动。若信任，当您下次登录时，系统将不会要求您提供验证码。对于HUAWEI STORE普通版脚本，每次运行脚本即创建一个新Chrome，信任意义不大，默认为0，建议设置为0
TRUST = 1

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
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+user + "抢购失败，再试一次")
            goToBuy(driver, user)
        else:
            if nowUrl != driver.current_url and driver.current_url != BUY_URL:
                print(user + ':成功！排队页面跳转了!!!!!!!!!!!!!!')
                submitOrder(driver, user)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+user + ':排队中')
                time.sleep(0.2)  # 排队中

#选择手机规格
def select(driver):
    if AUTO_COLOR==1:
        try:
            color = driver.find_element_by_link_text(COLOR);
            color.click()
            print(COLOR + '选择成功！')
        except:
            time.sleep(1)
            try:
                color = driver.find_element_by_link_text(COLOR);
                color.click()
                print(COLOR + '选择成功！')
            except:
                print('颜色选择错误！请手动选择！')
    else:
        print('无需选择颜色')

    if AUTO_EDITION==1:
        try:
            edition = driver.find_element_by_link_text(EDITION);
            edition.click()
            print(EDITION + '选择成功！')
        except:
            time.sleep(1)
            try:
                edition = driver.find_element_by_link_text(EDITION);
                edition.click()
                print(EDITION + '选择成功！')
            except:
                print('版本选择错误！请手动选择！')
    else:
        print('无需选择版本')

    if AUTO_COMBO==1:
        try:
            combo = driver.find_element_by_link_text(COMBO);
            combo.click()
            print(COMBO + '选择成功！')
        except:
            time.sleep(1)
            try:
                combo = driver.find_element_by_link_text(COMBO);
                combo.click()
                print(COMBO + '选择成功！')
            except:
                print('套餐选择错误！请手动选择！')
    else:
        print('无需选择套餐')

    print('手机规格全部选择成功')

# 登录成功去到购买页面
def goToBuy(driver, user):
    autoSelect=AUTO_SELECT
    driver.get(BUY_URL)
    time.sleep(0.5)
    if BUY_URL != driver.current_url:
        driver.get(BUY_URL)
    print(user + '打开购买页面')
    # 转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # 再次登陆
    try:
        denglu1 =  driver.find_element_by_id("top-index-loginUrl")
        denglu1.click()
        time.sleep(0.5)
    except:
        print(user + '已经登陆')
    # 结束标志位
    over = False
    time.sleep(0.5)
    if(autoSelect==1):
        select(driver)
    else:
        print('跳过选择配置')
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '开始检测')
        if time.time() > timestamp:  # 到了抢购时间
            text = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a')[0].text
            if text == '已售完':
                over = True
                break
            if text == '立即申购':
                buyButton = driver.find_element_by_link_text('立即申购')
                if buyButton.get_attribute('class') != 'product-button02 disabled':
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '可以开始申购，立即申购')
                    buyButton.click()
                    break
                else:
                    try:
                        textnext = driver.find_elements_by_xpath('//div[@id="pro-operation-countdown"]/p')[0].text
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '准备开始下一轮' + textnext + '的抢购')
                    except:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '准备开始下一轮的抢购')
            else:
                over = True
                break
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '等待0.2s，未到脚本开启时间，请选择好抢购的颜色、版本、套餐等：')
            time.sleep(0.2)
            
    if over:
        print("很遗憾，"+time.strftime("%H:%M:%S", time.localtime())+"抢购结束,程序将在60s后退出")
        time.sleep(60)
        driver.quit()
        exit()
    else:
        onQueue(driver, user)


# 登录商城,登陆成功后至商城首页然后跳转至抢购页面
def loginMall(user, pwd):
    option = webdriver.ChromeOptions()
    argument='--user-data-dir='+ personalDataPath
    option.add_argument(argument)
    print('配置成功')
    driver = webdriver.Chrome(executable_path=chrome_driver,options=option)
    print('webDriver打开成功')
    driver.get(LOGIN_URL)
    print('打开登陆页面')
    try:
        time.sleep(3)  # 等待页面加载完成
        account = driver.find_element_by_xpath('//input[@ht="input_pwdlogin_account"]')
        account.send_keys(user)
        password = driver.find_element_by_xpath('//input[@ht="input_pwdlogin_pwd"]')
        password.send_keys(pwd)
        denglu = driver.find_element_by_xpath('//div[@ht="click_pwdlogin_submitLogin"]')
        denglu.click()
        print(user + '成功输入了账号密码，尝试登陆.')
    except:
        print(user + '账号密码不能输入,请手动输入并登陆！')
    time.sleep(0.5)
    try:
        error=driver.find_element_by_xpath('//i[@class="ic-tips"]').text
        if error == '请输入图形验证码':
            denglu.click()
    except:
        time.sleep(0.1)
    isRemind=0
    while True:
        time.sleep(1)
        if LOGIN_SUCCESS_CONFIRM == driver.current_url:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + user + '登录成功！！')
            break
        else:
            if isRemind==0:
                print(user + '请手动完成认证并登陆！')
                isRemind=1
            try:
                isGetVerification=driver.find_element_by_xpath('//div[@ht="click_authentication_getAuthcode"]')
            except:
                print( '验证完毕')
                if TRUST==0:
                    try:
                        trust = driver.find_element_by_xpath('//div[@ht="click_dialog_leftbtn"]')
                        trust.click()
                    except:
                        print( '不信任出错，请自行点击不信任')
                if TRUST==1:
                    try:
                        trust = driver.find_element_by_xpath('//div[@ht="click_dialog_rightbtn"]')
                        trust.click()
                    except:
                        print( '信任出错，请自行点击信任')
                break
            if  isGetVerification.text == '获取验证码':
                print( '身份验证中')
                isGetVerification.click()
                print( '验证码已经发送')
            elif '重新获取' in isGetVerification.text:
                time.sleep(1)
            else:
                time.sleep(1)
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
        time.sleep(2)
        thr.start()
