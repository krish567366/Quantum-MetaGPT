from qmetagpt import (
    llm_paper_parser, 
    task_synthesizer,
    quantum_algorithm_generator,
    optimizer_engine,
    evaluation_engine,
    report_generator,
    security_licensing
)
from qmetagpt.utils.logger import get_logger
import os
import json

logger = get_logger(__name__)

def validate_license():
    license_manager = security_licensing.LicenseManager()
    if not os.path.exists("license.key"):
        logger.error("License file not found")
        return False
    
    with open("license.key", "rb") as f:
        license_key = f.read()
    
    return license_manager.validate_license(license_key)

def main(arxiv_id):
    # 1. License validation
    if not validate_license():
        logger.error("License validation failed. Exiting.")
        return
    
    logger.info("Starting QuantumMetaGPT pipeline")
    
    # 2. Parse paper
    paper = llm_paper_parser.parse_arxiv_paper(arxiv_id)
    llm_processor = llm_paper_parser.LLMProcessor()
    summary = llm_processor.summarize(paper['abstract'])
    pseudocode = llm_processor.extract_pseudocode(paper['abstract'])
    
    logger.info(f"Paper summary: {summary[:100]}...")
    
    # 3. Synthesize task
    synthesizer = task_synthesizer.TaskSynthesizer()
    task = synthesizer.synthesize(paper)
    
    # 4. Generate algorithm
    agent = quantum_algorithm_generator.get_agent(
        agent_name="PPO",
        state_dim=10,
        action_dim=5
    )
    agent.build_model()
    circuit = agent.generate_circuit(task)
    
    # 5. Optimize
    optimizer = optimizer_engine.HybridOptimizer(optimizer_type="COBYLA")
    optimized_params = optimizer.optimize(circuit, lambda params: 0.5)  # Placeholder cost function
    
    # 6. Evaluate
    evaluator = evaluation_engine.QuantumEvaluator(use_hardware=False)
    results = evaluator.evaluate(circuit)
    
    # 7. Generate report
    report_data = {
        "title": paper['title'],
        "metrics": {
            "fidelity": results.get('fidelity', 0.0),
            "execution_time": results['time'],
            "success": results['success']
        },
        "counts": results['counts'],
        "circuit": circuit
    }
    
    report_gen = report_generator.ReportGenerator()
    report_path = report_gen.generate(report_data)
    
    logger.info(f"Report generated at: {report_path}")
    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("arxiv_id", help="arXiv paper ID (e.g., quant-ph/1234567)")
    args = parser.parse_args()
    
    main(args.arxiv_id)