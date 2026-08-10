from pathlib import Path

from inference.image_detector import predict_ai_image
from inference.receipt_detector import verify_receipt
from inference.tampering_detector import predict_tampering


def print_result(title: str, result: dict) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not result.get("success"):
        print("FAILED")
        print("Error:", result.get("error"))
        return

    print("SUCCESS")
    print("Module:", result.get("module"))
    print("Prediction:", result.get("prediction"))
    print("Confidence:", result.get("confidence"))
    print("Risk Level:", result.get("risk_level"))
    print("Status:", result.get("status"))
    print("Processing Time:", result.get("processing_time_ms"), "ms")
    print("Visualization:", result.get("visualization_path"))
    print("Report:", result.get("report_path"))

    if result.get("decision_summary"):
        print("\nDecision Summary:")
        print(result["decision_summary"])


def main() -> None:
    print("Phase 3 backend test started")

    module1_image = Path("outputs/temp/test_module1.jpg")
    receipt_image = Path("outputs/temp/test_receipt.jpg")
    module3_image = Path("outputs/temp/test_module3.jpg")

    if module1_image.exists():
        print_result("Module 1 - AI Image Detection", predict_ai_image(module1_image))
    else:
        print("Module 1 skipped: outputs/temp/test_module1.jpg not found")

    if receipt_image.exists():
        print_result("Module 2 - Receipt Verification", verify_receipt(receipt_image))
    else:
        print("Module 2 skipped: outputs/temp/test_receipt.jpg not found")

    if module3_image.exists():
        print_result("Module 3 - Image Tampering Detection", predict_tampering(module3_image))
    else:
        print("Module 3 skipped: outputs/temp/test_module3.jpg not found")

    print("\nPhase 3 backend test completed")


if __name__ == "__main__":
    main()
