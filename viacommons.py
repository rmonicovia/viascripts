def _load_configs():
    import yaml
    import os

    with open('{HOME}/binvia/configs.yaml'.format(**os.environ)) as f:
        # TODO Melhorar isso
        return yaml.safe_load(f)


