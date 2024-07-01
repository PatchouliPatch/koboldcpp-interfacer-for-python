import requests
import json
import copy

class koboldcpp_interfacer:

    def __init__(self, url = "http://127.0.0.1:5001/",
                max_context_length = 8000, max_length = 1000,
                prompt = "test prompt", quiet = False, rep_pen = 1.1,
                rep_pen_range = 256, rep_pen_slope = 1, temperature = 0.5,
                tfs = 1, top_a = 0, top_k = 100, top_p = 0.9, typical = 1):

        """
        Template code for all variants.
        NOT INTENDED TO BE USED BY ITSELF.
        """

        self.target_url = url
        self.payload_template = {
            "max_context_length": max_context_length,
            "max_length": max_length,
            "prompt": prompt,
            "quiet": quiet,
            "rep_pen": rep_pen,
            "rep_pen_range": rep_pen_range,
            "rep_pen_slope": rep_pen_slope,
            "temperature": temperature,
            "tfs": tfs,
            "top_a": top_a,
            "top_k": top_k,
            "top_p": top_p,
            "typical": typical
        }

        self.header_template = {
            "Content-Type": "application/json"
        }

    def generate_reply(self, payload: str):

        pl = copy.deepcopy(self.payload_template)
        pl['prompt'] = payload

        response = self.send_to_server("/api/v1/generate", data = json.dumps(pl), header = self.header_template)
        if response[0] == 200:
            return (response[0], response[1]['results'][0]['text'],response[2])
        else:
            return (response[0], None, response[2])

    def tokenize(self, payload: str):

        for_check = {
            "prompt" : payload
        }

        return self.send_to_server('/api/extra/tokencount', json.dumps(for_check), self.header_template)
    
    def send_to_server(self, extension, data: str, header: dict):

        response = requests.post(self.target_url + extension, data = data, headers = header)

        if response.status_code == 200:
            result = response.json()
            return (response.status_code, result, response.text) # returns result json
        else:
            return (response.status_code, None, response.text)
        
    def set_generation_arg(self, key: str, val):

        if key not in self.payload_template.keys():

            return (400, "Key does not exist.", "Bad Request")
        
        else:

            if type(val) != type(self.payload_template[key]):

                return (400, f"Invalid value being assigned to key. Requires {type(val)}.", "Bad Request")

            self.payload_template[key] = val
            return (200, f"Template value updated. ({key} : {val})", "Ok")

# each class below just uses a specific formatter

class phi3_interfacer(koboldcpp_interfacer):

    # inherit from class above
    def __init__(self, url = "http://127.0.0.1:5001",
                max_context_length = 8000, max_length = 1000,
                prompt = "test prompt", quiet = False, rep_pen = 1.1,
                rep_pen_range = 256, rep_pen_slope = 1, temperature = 0.5,
                tfs = 1, top_a = 0, top_k = 100, top_p = 0.9, typical = 1):
        
        super().__init__(url, max_context_length, max_length, prompt, quiet,
                         rep_pen, rep_pen_range, rep_pen_slope, temperature,
                         tfs, top_a, top_k, top_p, typical)
        
    def single_inference(self, prompt: str):
        
        return self.chat_inference([{
            "role":"user",
            "content":prompt
        }])

    def chat_inference(self, back_and_forth: list, add_assistant_prompt = True, debug = False):

        for_inference = self.apply_phi3_format_list_of_entries(back_and_forth)
        if add_assistant_prompt: for_inference += '\n<|assistant|>'
        if debug:
            print('================================')
            print(for_inference)
            print('================================')
        return self.generate_reply(for_inference)

    def apply_phi3_format_str(self, prompt: str, role: str, prompt_assistant = True):

        if role == 'user':

            ret = f"<|user|>\n{prompt}<|end|>"

        elif role == 'assistant':

            ret = f"<|assistant|>\n{prompt}<|end|>"

        #if not role != 'assistant': ret += "\n<|assistant|>"

        return ret

    def apply_phi3_format_list_of_entries(self, prompt_list: list, debug = False):

        final_str = ""
        context_length = 1
        plist = copy.deepcopy(prompt_list)
        plist.reverse() # newest first, always

        for s in plist:
            
            to_add = self.apply_phi3_format_str(s['content'], s['role'])
            ctx_len = self.tokenize(to_add)[1]['value'] - 1

            if ctx_len + context_length <= self.payload_template['max_length']: 

                final_str = to_add + '\n' + final_str
                context_length += ctx_len

            else:
                break
        
        final_str = final_str.strip()
        
        if debug: print(context_length)
        return final_str