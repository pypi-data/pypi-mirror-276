from vtacML.pipeline import VTACMLPipe

if __name__ == '__main__':
    config_path = "config/config.yaml"
    vtac_ml = VTACMLPipe(config_path=config_path)

    best_model_paths = [
        # '../output/models/ada_grid_search.pkl',
        '../output/models/knn_grid_search.pkl',
        '../output/models/lr_grid_search.pkl',
        '../output/models/rfc_grid_search.pkl',
        '../output/models/svc_grid_search.pkl',
    ]
    for model in best_model_paths:
        vtac_ml.load_best_model(model_path=model, is_grid_search=True)
        vtac_ml.evaluate(name='seq0-1_' + model.split('/')[-1].split('_')[0], plot_extra=True)
