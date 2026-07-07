import requests
import json
from datetime import datetime

url = "http://localhost:8000/analyze"
payload = {
    "case_name": "TechFlow v. DataSync - Patent Infringement",
    "complaint_text": "Tech company accused of patent infringement on mobile payment processing system. Defendant has prior art from 2015, plaintiff filed patent in 2018. The patent covers a novel method for tokenizing payment credentials during mobile transactions.",
    "case_type": "IP",
    "urgency": "high",
    "additional_context": "Defendant has prior art from 2015, plaintiff filed patent in 2018"
}

print("Sending request to API...")
response = requests.post(url, json=payload)
data = response.json()

# Pretty-print to terminal
print(json.dumps(data, indent=2))

# Save to final_report.md
with open("final_report.md", "w") as f:
    f.write("# Legal Intelligence AI System — Final Report\n\n")
    f.write(f"Generated: {datetime.now().isoformat()}\n\n")
    f.write("## API Response\n\n")
    f.write("```json\n")
    f.write(json.dumps(data, indent=2))
    f.write("\n```\n\n")
    
    f.write("## Section Summary\n\n")
    for section in data.get("sections", []):
        f.write(f"### {section['title']}\n")
        f.write(f"- Agent: {section['agent_type']}\n")
        f.write(f"- Quality Score: {section['quality_score']:.3f}\n")
        f.write(f"- Tokens: {section['tokens_used']}\n")
        f.write(f"- Cost: ${section['cost']:.6f}\n\n")
        f.write(f"{section['content'][:500]}...\n\n")
    
    f.write(f"## Summary Stats\n\n")
    f.write(f"- Total Cost: ${data.get('total_cost', 0):.6f}\n")
    f.write(f"- Total Tokens: {data.get('total_tokens', 0)}\n")
    f.write(f"- Processing Time: {data.get('processing_time', 0):.2f}s\n")
    f.write(f"- Confidence Score: {data.get('confidence_score', 0):.3f}\n")

print("\n✅ Report saved to final_report.md")