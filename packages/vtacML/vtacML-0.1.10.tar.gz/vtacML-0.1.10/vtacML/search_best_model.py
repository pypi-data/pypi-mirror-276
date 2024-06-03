from .pipeline import VTACMLPipe

if __name__ == "__main__":
    config_path = "config/config.yaml"
    vtac_ml = VTACMLPipe(config_path=config_path)

    vtac_ml.train()
    vtac_ml.save_best_model()