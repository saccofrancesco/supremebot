# Importing Libraries
from playwright.sync_api import sync_playwright, TimeoutError
import json
import playwright

# Creating the Bot Class


class Bot:

    # Constructor
    def __init__(self) -> None:

        # Opening the Items File
        with open("./config/items.json", "r") as i:

            # Loading the JSON File
            ITEMS: str = json.load(i)

            # Creating the Lists
            self.ITEMS_NAMES: list = []
            self.ITEMS_STYLES: list = []
            self.ITEMS_SIZES: list = []
            self.ITEMS_TYPES: list = []

            # Looping the JSON File
            for item in ITEMS:

                # Appending the Prameters to the Lists
                self.ITEMS_NAMES.append(item["name"])
                self.ITEMS_STYLES.append(item["color"])
                self.ITEMS_SIZES.append(item["size"])
                # Preventing tops/sweaters to make error in the link
                self.ITEMS_TYPES.append(item["category"].replace("/", "-"))

        # Opening the Data File
        with open("./config/pay.config.json", "r") as d:

            # Loading the JSON File
            DATA: str = json.load(d)

            # Looping the JSON File
            for info in DATA:

                # Storing Personal Data
                self.EMAIL: str = info["email"]
                self.COUNTRY: str = info["country"]
                self.FIRST_NAME: str = info["first_name"]
                self.LAST_NAME: str = info["last_name"]
                self.ADDRESS: str = info["address"]
                self.POSTAL_CODE: str = info["postal_code"]
                self.CITY: str = info["city"]
                self.PHONE: str = info["phone"]
                self.CARD_NUMBER: str = info["card_number"]
                self.MONTH_EXP: str = info["expiration_month"]
                self.YEAR_EXP: str = info["expiration_year"]
                self.CVV: str = info["cvv"]
                self.NAME_ON_CARD: str = info["name_on_card"]
                try:
                    self.ZONE: str = info["zone"]
                except Exception:
                    pass

        # Creating the Link's List
        self.links_list: list = []

    def scrape(self) -> None:
        for i in range(len(self.ITEMS_NAMES)):
            url: str = f"https://jp.supreme.com/collections/{self.ITEMS_TYPES[i]}"
            print(f"Processing {self.ITEMS_NAMES[i]}...")

            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True, args=["--no-images"])
                page = browser.new_page()

                # ページの読み込みレベルを調整
                page.goto(url, wait_until="domcontentloaded")

                # 商品一覧から必要な情報を収集
                product_elements = page.query_selector_all(
                    "li.collection-product-item")
                temp_links = []
                for element in product_elements:
                    # 売り切れや非表示のアイテムをスキップ
                    if element.get_attribute("data-available") == "false":
                        continue

                    product_name_elm = element.query_selector(
                        "span.collection-product-info--title")
                    if product_name_elm is None:
                        continue
                    product_name = product_name_elm.inner_text()
                    if product_name == self.ITEMS_NAMES[i]:
                        product_link = element.query_selector(
                            "a[data-cy-title]").get_attribute("href")
                        complete_link = f"https://jp.supreme.com{product_link}"
                        temp_links.append(complete_link)

                for complete_link in temp_links:
                    page.goto(complete_link)  # Navigate to the link
                    product_style_element = page.query_selector(
                        "#product-root > div > div.Product.width-100.js-product.routing-transition.fade-on-routing > div.product-column-left.bpS-bg-none.bg-white.mobile-shadow.pt-s.pb-s.bpS-pt-0.bpS-pb-0.position-relative.pr-0.bpS-pr-s > div.product-title-container.bpS-display-none.pl-s.pr-s > div")

                    product_style_text = product_style_element.inner_text()

                    if product_style_text == self.ITEMS_STYLES[i]:
                        self.links_list.append(complete_link)
                        break

                browser.close()

    # Method for Add to the Cart the founded Items

    def add_to_basket(self, page) -> None:

        # Looping the Element's to Buy List
        for i in range(len(self.links_list)):
            page.goto(self.links_list[i])
            if self.ITEMS_TYPES[i] == "bags":
                page.click("input[data-type='product-add']")
                page.wait_for_timeout(1000)
                continue
            page.wait_for_selector("select[data-cy='size-selector']")
            options = page.locator("select[data-cy='size-selector']")
            options.select_option(label=f"{self.ITEMS_SIZES[i]}")
            page.click("input[data-type='product-add']")
            page.wait_for_timeout(1000)

    # Method for Compiling the Checkout Form

    def checkout(self, page) -> None:

        # Going to the Checkout
        try:
            # Increased timeout
            page.click('#product-root > div > div.collection-nav.display-none.bpS-display-block > div > div > div > a.button.button--s.c-white.width-100.display-flex.bg-red--aa', timeout=60000)
        except TimeoutError:
            pass

        # Using Data to Compile the Form
        page.fill("input[id='email']", self.EMAIL)
        page.fill("input[name='firstName']", self.FIRST_NAME)
        page.fill("input[name='lastName']", self.LAST_NAME)
        page.fill("input[id='postalCode']", self.POSTAL_CODE)
        page.fill("input[name='address1']", self.ADDRESS)
        page.fill("input[name='address2']", "建物番号")
        page.fill("input[name='city']", self.CITY)
        page.fill("input[name='phone']", self.PHONE)
        try:
            page.wait_for_selector("select[name='zone']")
            options = page.locator("select[name='zone']")
            options.select_option(value="JP-13")  # 例として "JP-13" を選択
            page.wait_for_timeout(1500)  # 配送情報を待機
        except Exception as e:
            print(e)

       # カード番号のiframeを特定して、iframe内の要素にアクセスして値を入力
        page.frame_locator(
            "iframe[src*='checkout.shopifycs.com/number']").locator("input[name='number']").fill(self.CARD_NUMBER)
        # 有効期限のiframeを特定して、iframe内の要素にアクセスして値を入力
        page.frame_locator("iframe[src*='checkout.shopifycs.com/expiry']").locator(
            "input[name='expiry']").fill(f"{self.MONTH_EXP}/{self.YEAR_EXP}")
        # CVV番号のiframeを特定して、iframe内の要素にアクセスして値を入力
        page.frame_locator("iframe[src*='checkout.shopifycs.com/verification_value']").locator(
            "input[name='verification_value']").fill(self.CVV)
        # カード名義人の名前のiframeを特定して、iframe内の要素にアクセスして値を入力
        page.frame_locator(
            "iframe[src*='checkout.shopifycs.com/name']").locator("input[name='name']").fill(self.NAME_ON_CARD)
        # チェックボックスを特定してチェックを入れる
        # チェックボックスのラベルテキストを使って要素を特定してチェックを入れる
        page.evaluate(
            "() => document.querySelectorAll('input[type=checkbox]')[1].click()")

        # '購入する' ボタンをクリック
        page.click("button[type='submit']")
