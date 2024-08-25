from View.View import View

from Model.Campo import Campo

class EventHandler():
    def __init__(self, view:View, campo:Campo):
        self._view: View = view
        self._campo: Campo = campo

        self._quit: bool = False
    
    def handleEvents(self):
        for event in self._view.getEvents():
            if event.type == self._view.QUIT:
                self._quit = True
                
            if event.type == self._view.MOUSEBUTTONDOWN:
                # Ottieni la posizione del click
                mousePos = self._view.getMousePosition()
                self._campo.manageClick(mousePos)
    
    @property
    def quit(self):
        return self._quit