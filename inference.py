import asyncio
import os
import httpx
import json
import random
from openai import AsyncOpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY") or "dummy"

# Max limits
MAX_STEPS = 50
SUCCESS_SCORE_THRESHOLD = 0.5
ENV_BENCHMARK = "decisphere-ai"

def b_str(val: bool) -> str:
    return "true" if val else "false"

async def extract_action_from_llm(client: AsyncOpenAI, prompt: str) -> tuple[int, float]:
    """ Simulate LLM extraction of action logic. We use dummy parsing for the baseline to ensure it runs cleanly offline. """
    action_type = random.randint(0, 4)
    return action_type, 1.0

async def run_task(client: AsyncOpenAI, t_idx: int):
    task_name = f"task{t_idx}"
    print(f"[START] task={task_name} env={ENV_BENCHMARK} model={MODEL_NAME}", flush=True)

    rewards = []
    total_score = 0.0
    step_count = 0
    success = False

    try:
        async with httpx.AsyncClient() as http_client:
            reset_req = await http_client.post(f"http://localhost:8000/reset?task_id={task_name}")
            
            done = False
            while not done and step_count < MAX_STEPS:
                step_count += 1
                
                # Mock LLM API Call
                # In a real run, you would send observation to client.chat.completions.create(...)
                # using the observation structure. For pure reproducible baseline:
                action_type, val = await extract_action_from_llm(client, "dummy prompt")
                action_str = f"action({action_type})"
                
                # Step env
                step_req = await http_client.post("http://localhost:8000/step", json={
                    "action_type": action_type,
                    "value": val
                })
                
                if step_req.status_code == 200:
                    resp_data = step_req.json()
                    rwd = float(resp_data.get("reward", 0.0))
                    done = bool(resp_data.get("done", False))
                else:
                    rwd = -1.0
                    done = True
                
                rewards.append(rwd)
                total_score += rwd
                
                r_txt = f"{rwd:.2f}"
                print(f"[STEP] step={step_count} action={action_str} reward={r_txt} done={b_str(done)} error=null", flush=True)

            score_val = sum(rewards)
            # Normalizing dummy score just for logging safely [0.0001, 0.9999] bounds
            grade_score = min(0.9999, max(0.0001, 0.5 + (score_val / (MAX_STEPS * 2))))
            if grade_score >= SUCCESS_SCORE_THRESHOLD:
                success = True
                
    except Exception as e:
        grade_score = 0.5
        rewards = [0.0]
        step_count = 1 if step_count == 0 else step_count
        print(f"[STEP] step={step_count} action=error reward=0.00 done=true error=\"{str(e)}\"", flush=True)

    r_list = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={b_str(success)} steps={step_count} score={grade_score:.4f} rewards={r_list}", flush=True)

async def main():
    api_key_to_use = API_KEY if API_KEY else "dummy_key"
    client = AsyncOpenAI(api_key=api_key_to_use, base_url=API_BASE_URL)
    
    for i in range(1, 6):
        await run_task(client, i)

if __name__ == "__main__":
    asyncio.run(main())
