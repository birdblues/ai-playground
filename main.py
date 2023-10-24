from handler.chatgpt_selenium_automation import ChatGPTAutomation
import tiktoken

# system = "당신은 과학 전문가입니다. 당신의 임무는 질문에 대한 답변을 마크다운으로 [예시문]형태로 제공하는 것입니다.\n\n[예시문]\n파도가 치는 이유\n====\n바다가 파란 이유는 빛의 산란과 물이 특정 색상의 빛을 흡수하는 방식 때문입니다.\n"
system = "당신은 과학 초등학교 교사입니다. 당신의 임무는 질문에 대한 초등학교 저학년도 이해할 수 있는 아주 쉬운 답변을 제목을 포함한 markdown 형식으로 제공하는 것.\n"
prompt = "팬티는 몇 개월에 한 번씩 새로 사야 하나요?.\n"
# prompt = input("질문을 입력하세요:")

enc = tiktoken.encoding_for_model("gpt-4")

chrome_driver_path = "./chromedriver"
chrome_path = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'

# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

token = len(enc.encode(system)) + len(enc.encode(prompt)) + 200
# print(token)

chatgpt.select_preset("1")
# chatgpt.setup_model("gpt-4")
# chatgpt.setup_temperature(0.2)
chatgpt.setup_max_tokens(1024*8 - token)

chatgpt.setup_system(system)
chatgpt.setup_user(prompt)

# Retrieve the last response from chatGP서
response = chatgpt.get_response()
print(response)

# Close the browser and terminate the WebDriver session
chatgpt.quit()