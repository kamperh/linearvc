dependencies = ["torch", "torchaudio", "numpy", "celer"]

from linearvc import LinearVC


def get_linearvc(progress=True, device="cuda"):
    wavlm = torch.hub.load(
        "bshall/knn-vc",
        "wavlm_large",
        trust_repo=True,
        progress=progress,
        device=device,
    )
    hifigan, _ = torch.hub.load(
        "bshall/knn-vc",
        "hifigan_wavlm",
        trust_repo=True,
        prematched=True,
        progress=progress,
        device=device,
    )

    linearvc_model = LinearVC(wavlm, hifigan, device)

    return linearvc_model
