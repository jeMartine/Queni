from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome() 

driver.get("http://localhost:8000/") 

fecha_inicio_input = driver.find_element_by_name("fecha_inicio")
fecha_inicio_input.send_keys("2023-08-01")  

fecha_fin_input = driver.find_element_by_name("fecha_fin")
fecha_fin_input.send_keys("2023-08-31")

generar_informe_button = driver.find_element_by_css_selector("button[type='submit']")
generar_informe_button.click()


driver.implicitly_wait(10)


enlace_descarga = driver.find_element_by_link_text("Descargar Informe en PDF")
assert enlace_descarga.is_displayed()

driver.quit()
