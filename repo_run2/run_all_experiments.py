import os
import sys
import time
import subprocess

def run_step(step_name, cmd):
    print(f"\n{'='*75}")
    print(f"  EXECUTING PIPELINE STEP: {step_name}")
    print(f"  Command: {cmd}")
    print(f"{'='*75}\n")
    t0 = time.time()
    res = subprocess.run(cmd, shell=True)
    elapsed = time.time() - t0
    if res.returncode != 0:
        print(f"\n[ERROR] Step '{step_name}' failed with exit code {res.returncode} after {elapsed:.1f}s!")
        sys.exit(res.returncode)
    print(f"\n[SUCCESS] Step '{step_name}' completed in {elapsed:.1f}s.")

def main():
    py_exec = sys.executable
    t_start = time.time()
    print("*************************************************************************")
    print("  LAUNCHING FULL EXPERIMENT REPRODUCTION PIPELINE (RUN 2)")
    print("*************************************************************************")
    
    # 1. Run E0 Baseline (Prompted 1.5B LLM)
    run_step("E0 Base Agent Inference", f"{py_exec} -u repo_run2/src/agent/run_e0.py")
    
    # 2. Generate Calibration Split Outputs
    run_step("Calibration Split Inference", f"{py_exec} -u repo_run2/src/generate_cal_and_math.py")
    
    # 3. Train E2 0.5B Sequence Classifier (LoRA + Classification Head)
    run_step("E2 0.5B Classifier Training", f"{py_exec} -u repo_run2/src/e2_classifier/train_classifier_real.py")
    
    # 4. Train E1 Policy Models via GRPO (RLVR vs RLCR)
    run_step("E1 GRPO Policy Training (RLVR & RLCR)", f"{py_exec} -u repo_run2/src/e1_rlcr/train_grpo_real.py")
    
    # 5. Evaluate Trained RL Checkpoints (Batched Inference)
    run_step("E1 Policy Batched Evaluation", f"{py_exec} -u repo_run2/src/e1_rlcr/eval_rl_checkpoints.py")
    
    # 6. Run Orchestrator (E3, E4, Table, Figures, Failure Taxonomy)
    run_step("Master Orchestration & Analysis", f"{py_exec} -u repo_run2/src/orchestrator.py")
    
    total_elapsed = time.time() - t_start
    print(f"\n{'*'*75}")
    print(f"  ALL EXPERIMENTS COMPLETED SUCCESSFULLY IN {total_elapsed/60:.2f} MINUTES!")
    print(f"{'*'*75}\n")

if __name__ == "__main__":
    main()
