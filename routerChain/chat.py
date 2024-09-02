from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0)
chat_prompt = """你是一个聊天助手，你将根据用户与你的互动，结合你的认知回答用户的问题。这是一个问题：
                {input}"""
operation_prompt = """你是一个可以控制个人电脑的智能助手，你将根据用户提出的需求返回指定格式的电脑控制指令。
                这是一个需求：{input}"""

prompt_infos = [
  {
    '名字': '聊天',
    '描述': '作为聊天助手与用户互动聊天。',
    '提示模板': chat_prompt
  },
  {
    '名字': '电脑控制',
    '描述': '根据用户的电脑使用需求给出指定格式的电脑控制指令。',
    '提示模板': operation_prompt
  }
]

destination_chains = {}
for p_info in prompt_infos:
  name = p_info['名字']
  prompt_template = p_info['提示模板e']
  prompt = ChatPromptTemplate.form_template(template=prompt_template)
  chain = LLMChain(llm=llm, prompt=prompt)
  destination_chains[name] = chain
destinations = [f"{p['名字']}: {p['描述']}" for p in prompt_infos]
destinations_str = '\n'.join(destinations)
default_prompt = ChatPromptTemplate.from_template('{input}')
default_chain = LLMChain(llm=llm, prompt=default_prompt)

MULTI_PROMPT_ROUTER_TEMPLATE = """给语言模型一个原始文本输入，让其选择最合适输入的模型提示模板。
                                  系统将为你提供可用的提示模板的名称以及最适合该提示的描述。
                                  如果你认为修改原始输入最终会导致语言模型做出更好的响应，
                                  你也可以修改原始输入。
                                  <<格式>>
                                  返回一个带有JSON对象的markdown代码片段，该JSON对象的格式如下：
                                  '''json
                                  {{{{
                                    'destination': 字符串/使用的提示名字或者使用'DEFAULT',
                                    'next_inputs': 字符串/原始输入的改进版本
                                  }}}}
                                  '''
                                  记住：'destination'必须是下面指定的候选提示名字之一，
                                  或者如果输入不太合适任何候选提示，则可以是'DEFAULT'。
                                  记住：如果你认为不需要任何修改，则'next_inputs'可以只是原始输入。
                                  <<候选提示>>
                                  {destinations}
                                  <<输入>>
                                  {{input}}
                                  <<输出（务必要包含'''json）>>

                                  样例：
                                  <<输入>>
                                  "打开谷歌浏览器。"
                                  <<输出>>
                                  '''json
                                  {{{{
                                    'destination': 字符串/使用的提示名字或者使用'DEFAULT',
                                    'next_inputs': 字符串/原始输入的改进版本
                                  }}}}
                                  '''
                                """

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
  destinations=destinations_str
)
router_prompt = PromptTemplate(
  template=router_template,
  input_variables = ['input'],
  output_parser=RouterOutputParser()
)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

chain = MultiPromptChain(router_chain=router_chain,
                        destination_chains=destination_chains,
                         default_chain=default_chain,
                         verbose=False
                        )

if __name__=='__main__':
    chain.run("打开谷歌浏览器")
