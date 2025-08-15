import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def human_like_actions(driver, moves=5):
    """
    Simula movimientos y acciones humanas aleatorias en el navegador
    y siempre hace scroll up al final sin salirse de la ventana.
    """
    actions = ActionChains(driver)

    # Obtener tamaño de ventana para evitar salirse
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    for _ in range(moves):
        action_type = random.choice(["mouse_move", "scroll", "key_press"])

        if action_type == "mouse_move":
            # Movimientos pequeños para no salirnos de la ventana
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            try:
                actions.move_by_offset(x_offset, y_offset).perform()
            except:
                # Si falla el movimiento, reiniciamos el cursor al centro
                actions.move_to_element(driver.find_element("tag name", "body")).perform()

        elif action_type == "scroll":
            scroll_amount = random.randint(-200, 200)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        elif action_type == "key_press":
            key = random.choice([Keys.ARROW_DOWN, Keys.ARROW_UP, Keys.TAB])
            actions.send_keys(key).perform()

        # Pausa aleatoria
        time.sleep(random.uniform(0.5, 2))

    # 📌 Siempre volver al inicio
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(0.5, 1.5))
