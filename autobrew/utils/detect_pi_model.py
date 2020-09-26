def detect_pi_model() -> int:
    f = open("/proc/device-tree/model", "r")
    model_text = f.read()
    if model_text.startswith("Raspberry Pi 4"):
        return 4
    elif model_text.startswith("Raspberry Pi 3"):
        return 3
    elif model_text.startswith("Raspberry Pi 2"):
        return 2
    else:
        raise RuntimeError("Could not determine pi version")
