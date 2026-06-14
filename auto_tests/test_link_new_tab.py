from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

LOGIN_URL = "https://id.skyeng.ru/login?redirect=https%3A%2F%2Fteacher.skyeng.ru%2F"
EMAIL = "test.tst317@skyeng.ru"
PASSWORD = "Abc1234567890"

try:
    print("1. Открываем страницу логина...")
    driver.get(LOGIN_URL)
    time.sleep(3)

    print("2. Ищем кнопку 'Войти с помощью пароля'...")
    password_login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-send-otp-form-to-username-password"))
    )
    password_login_link.click()
    time.sleep(2)

    print("3. Вводим email...")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    email_input.send_keys(EMAIL)

    print("4. Вводим пароль...")
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)

    print("5. Нажимаем кнопку входа...")
    login_button = driver.find_element(By.CSS_SELECTOR, "button.button--primary")
    login_button.click()
    time.sleep(5)

    print("6. Переходим в расписание...")
    driver.get("https://teacher.skyeng.ru/schedule")
    time.sleep(5)

    print("7. Ищем кнопку 'Создать'...")
    create_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Создать')]"))
    )
    create_btn.click()
    print("   ✅ Нажали 'Создать'")
    time.sleep(2)

    print("8. Ищем и нажимаем 'Личное событие'...")
    personal_event = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Личное событие')]"))
    )
    personal_event.click()
    print("   ✅ 'Личное событие' выбрано")
    time.sleep(2)

    print("9. Заполняем название события...")
    title_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Например: посмотреть вебинар']"))
    )
    title_input.send_keys("Автотест ссылки")
    print("   ✅ Название введено")

    print("10. Заполняем описание ссылкой...")
    desc_input = driver.find_element(By.XPATH, "//textarea[@placeholder='Например: ссылка на вебинар']")
    desc_input.send_keys("https://example.com")
    print("   ✅ Описание введено")

    # НАДЁЖНЫЙ ПОИСК КНОПКИ "СОХРАНИТЬ"
    print("11. Ищем кнопку 'Сохранить' по классу...")
    
    # Пробуем найти по точному классу (без учёта порядка)
    save_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.-size-m.root"))
    )
    print(f"   ✅ Нашли кнопку: текст='{save_btn.text}'")
    
    driver.execute_script("arguments[0].click();", save_btn)
    print("   ✅ Сохранение нажато")
    time.sleep(3)

    print("12. Ищем созданное событие в календаре...")
    event = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Автотест ссылки')]"))
    )
    event.click()
    print("   ✅ Событие открыто")
    time.sleep(2)

    print("13. Ищем ссылку в описании...")
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'example.com')]"))
    )
    link.click()
    print("   ✅ По ссылке кликнули")
    time.sleep(2)

    print("14. Проверяем количество вкладок...")
    assert len(driver.window_handles) == 2, "❌ Новая вкладка не открылась"
    print("   ✅ Новая вкладка открылась")

    print("15. Переключаемся на новую вкладку...")
    driver.switch_to.window(driver.window_handles[1])
    assert "example.com" in driver.current_url, "❌ Ссылка открылась не там"
    print("   ✅ URL совпадает")

    print("\n✅✅✅ ТЕСТ ПРОЙДЕН УСПЕШНО! ✅✅✅")

except Exception as e:
    print(f"\n❌ Тест упал на шаге с ошибкой: {e}")

finally:
    time.sleep(5)
    driver.quit()
