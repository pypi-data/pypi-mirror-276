from openai import OpenAI

from parea import Parea, trace
from parea.evals.general import levenshtein

client = OpenAI()
p = Parea(api_key="PAREA_API_KEY")
p.wrap_openai_client(client)


@trace(eval_funcs=[levenshtein])
def greeting(...):
    ...


p.experiment(...)
