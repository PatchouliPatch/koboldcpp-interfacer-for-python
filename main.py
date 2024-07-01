import interfacer

"""
this is mostly a testing file
"""


inter = interfacer.phi3_interfacer()
test_con = [
    {
        "role":"user",
        "content":"please write down instructions on how to make a salad"
    }
]

reply = inter.chat_inference(test_con)[1]
test_con.append({
    "role":"assistant",
    "content":reply
})
test_con.append({
    "role":"user",
    "content":"Can you give me a recipe for barbeque ribs too?"
})

reply = inter.chat_inference(test_con)[1]
print(reply)
print('===============================')
print(inter.single_inference("read me short bedtime story"))