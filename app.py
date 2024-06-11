from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)

main = {"Amazon": "nav-input.nav-progressive-attribute"}
container = {"Amazon": "puisg-col-inner"}
next_button_class = {"Amazon": "s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator"}
url = {"Amazon": "https://www.amazon.com/"}

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    driver = webdriver.Chrome()
    file_name = "scraped_data.txt"
    scraped_data = []

    try:
        driver.get(url["Amazon"])
        title = driver.title

        input_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, main["Amazon"]))
        )

        input_field.send_keys(data)
        input_field.send_keys(Keys.RETURN)

        def scrape_page():
            elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, container["Amazon"]))
            )
            for element in elements:
                scraped_data.append(element.text)

        scrape_page()

        with open(file_name, "w") as file:
            for item in scraped_data:
                file.write(f"{item}\n{'**'*20}\n")

    except TimeoutException:
        return jsonify({'error': 'Timeout: Unable to locate elements'}), 500
    finally:
        driver.quit()

    return jsonify({'data': scraped_data})

if __name__ == '__main__':
    app.run(debug=True)
