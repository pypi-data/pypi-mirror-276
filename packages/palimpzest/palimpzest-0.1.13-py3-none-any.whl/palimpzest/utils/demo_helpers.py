from palimpzest.execution import flatten_nested_tuples
from itertools import pairwise
import gradio as gr
import pandas as pd

def createPlanStr(flatten_ops):
  """Helper function to return string w/physical plan."""
  plan_str = ""
  start = flatten_ops[0]
  plan_str += f" 0. {type(start).__name__} -> {start.outputSchema.__name__} \n"

  for idx, (left, right) in enumerate(pairwise(flatten_ops)):
      in_schema = left.outputSchema
      out_schema = right.outputSchema
      plan_str += f" {idx+1}. {in_schema.__name__} -> {type(right).__name__} -> {out_schema.__name__} "

      if right.is_hardcoded():
          plan_str += f"\n    Using hardcoded function"
      elif hasattr(right, 'model'):
          plan_str += f"\n    Using {right.model}"
          if hasattr(right, 'filter'):
              filter_str = right.filter.filterCondition if right.filter.filterCondition is not None else str(right.filter.filterFn)
              plan_str += f'\n    Filter: "{filter_str}"'
          if hasattr(right, 'token_budget'):
              plan_str += f'\n    Token budget: {right.token_budget}'
          if hasattr(right, 'query_strategy'):
              plan_str += f'\n    Query strategy: {right.query_strategy}'
      plan_str += "\n"
      plan_str += f"    ({','.join(in_schema.fieldNames())[:15]}...) -> ({','.join(out_schema.fieldNames())[:15]}...)"
      plan_str += "\n\n"

  return plan_str


def printTable(records, cols=None, query=None, plan=None):
    """Helper function to print execution results using Gradio"""
    if len(records) == 0:
      print("No records met search criteria")
      return

    records = [
        {
            key: record.__dict__[key]
            for key in record.__dict__
            if not key.startswith('_')
        }
        for record in records
    ]
    records_df = pd.DataFrame(records)
    print_cols = records_df.columns if cols is None else cols

    with gr.Blocks() as demo:
        gr.Dataframe(records_df[print_cols])

        if plan is not None:
            # plan_str = buildNestedStr(plan.dumpPhysicalTree())
            ops = plan.dumpPhysicalTree()
            flatten_ops = flatten_nested_tuples(ops)
            plan_str = createPlanStr(flatten_ops)
            gr.Textbox(value=plan_str, info="Physical Plan")

    demo.launch()
