from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def is_alert_present(driver):
    try:
        driver.find_element("xpath", "/html/body/div[2]/div[4]/div/div[6]/div[7]/button").click()
        return False
    except:
        return True

def gogogo(driver, check_flag):
    outer_iframe = driver.find_elements(By.TAG_NAME, "iframe")
    print(outer_iframe)
    driver.switch_to.frame(outer_iframe[0])
    state = driver.find_element("xpath", "//*[@id=\"ext-gen1050\"]").get_attribute("class")
    print(state)
    inner_iframe = driver.find_elements(By.TAG_NAME, "iframe")
    print("inner_iframe:" + str(len(inner_iframe)))
    missions = len(inner_iframe)
    videos = driver.find_elements("xpath", "//*[@id=\"ext-gen1049\"]")
    for video_index in range(len(videos)):
        if videos[video_index].get_attribute("class") == "ans-attach-ct":
            driver.switch_to.frame(inner_iframe[video_index])
            watch_video(driver, video_index, inner_iframe, check_flag)
    pdfs = missions - len(videos)
    for pdf_index in range(pdfs):
        driver.switch_to.frame(inner_iframe[len(videos) + pdf_index])
        watch_pdf(driver)
    driver.switch_to.default_content()

def watch_video(driver, video_index, inner_iframe, check_flag):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div/button")))
    driver.find_element("xpath", "/html/body/div[2]/div[4]/div/button").click()
    driver.find_element("xpath", "/html/body/div[2]/div[4]/div/div[6]/div[1]/button").click()
    time.sleep(0.2)
    driver.find_element("xpath", "/html/body/div[2]/div[4]/div/div[6]/div[1]/button").click()
    time.sleep(0.2)
    driver.find_element("xpath", "/html/body/div[2]/div[4]/div/div[6]/div[1]/button").click()
    time.sleep(0.2)
    print(video_index)
    driver.switch_to.parent_frame()
    while driver.find_elements("xpath", "//*[@id=\"ext-gen1049\"]")[video_index].get_attribute(
            "class") != "ans-attach-ct ans-job-finished":  # 观看状态
        print("watching now...")
        if check_flag == 1:
            driver.switch_to.frame(inner_iframe[video_index])
            i = 1
            while is_alert_present(driver):
                driver.find_element("xpath", "//*[@class=\"tkTopic_con tkScroll\"]/div/ul/li[{_i}]/label".format(_i=i)).click()
                i = i + 1
                time.sleep(0.2)
                driver.find_element("xpath", "//*[@id=\"videoquiz-submit\"]").click()
                time.sleep(0.2)
            driver.switch_to.parent_frame()
        time.sleep(1)

def watch_pdf(driver):
    innest_iframe = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(innest_iframe[0])
    for page in range(1, 1000):
        try:
            img = driver.find_element("xpath", "/html/body/div[1]/img[{_i}]".format(_i=page))
            driver.execute_script("arguments[0].scrollIntoView(false);", img)
        except:
            driver.switch_to.parent_frame()
            driver.switch_to.parent_frame()
            break

options = Options()
options.headless = False
# option = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
DRIVER_PATH = '文件路径\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
allhandles=driver.window_handles
nowhandle = driver.current_window_handle


time.sleep(0.5)
driver.get("http://i.mooc.ecourse.ucas.ac.cn/space/index")
driver.maximize_window()
time.sleep(10)
driver.execute_script('window.open("复制的链接")')     #详情见README.md
time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
des = ''
check_flag = 1
for capter in range(1,11):
    state = ''
    for i in range(1,12):
        try:
            xpath = "/html/body/div[5]/div[1]/div[2]/div[3]/div[{_capter}]/div[{_i}]/h3/a/span[2]/em".format(_capter = capter, _i = i)
            state = driver.find_element(By.XPATH, xpath).get_attribute("class")
            if state == "orange":
                des = "/html/body/div[5]/div[1]/div[2]/div[3]/div[{_capter}]/div[{_i}]/h3/a/span[3]".format(_capter = capter, _i = i)
                check_flag = 0 if i == 1 else 1
                break
        except:
            continue
    if state == "orange":
        break
driver.find_element("xpath", des).click()
time.sleep(2)
gogogo(driver, check_flag)

for capter in range(1,11):
    for i in range(1,12):
        try:
            check_flag = 0 if i == 1 else 1
            xpath = "/html/body/div[4]/div[1]/div[2]/div[1]/div/div[{_capter}]/div[{_i}]/h4/span[2]".format(_capter = capter, _i = i)
            state = driver.find_element(By.XPATH, xpath).get_attribute("class")
            if state == "roundpointStudent  orange01 a002 jobCount":
                des = "/html/body/div[4]/div[1]/div[2]/div[1]/div/div[{_capter}]/div[{_i}]/h4/a".format(_capter = capter, _i = i)
                driver.find_element("xpath", des).click()
                time.sleep(2)
                gogogo(driver, check_flag)
            else:
                continue
        except:
            break


