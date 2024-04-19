

class ModelPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # self.view.presenter = self

    def load_ai_models(self):
        ai_models = self.model.load_ai_models()
        self.view.predict.ai_models = ai_models
        self.view.predict.update_models()
