from .models import EloParameter

START_ELO = 1000
K_INDEX = 32
SCALE_FACTOR = 400

class Parameters:
    def __init__(self) -> None:
        self._start_elo = None
        self._k_index = None
        self._scale_factor = None
        self.sync_with_db_or_set_default()

    def sync_with_db_or_set_default(self):
        # get values from database and set them
        parameters = EloParameter.objects.order_by('-created_at').first()
        if parameters:
            self._start_elo = parameters.start_elo
            self._k_index = parameters.k_index
            self._scale_factor = parameters.scale_factor
        else:
            self._start_elo = START_ELO
            self._k_index = K_INDEX
            self._scale_factor = SCALE_FACTOR
            
            p = EloParameter(
                start_elo = self._start_elo,
                k_index = self._k_index,
                scale_factor = self._scale_factor
            )
            p.save()


    @property
    def start_elo(self):
        return self._start_elo

    @start_elo.setter
    def start_elo(self, value: int) -> None:
        if not value:
            raise ValueError("start_elo cannot be empty")
        self._start_elo = value

    @property
    def k_index(self) -> int | float:
        return self._k_index

    @property
    def scale_factor(self) -> int | float:
        return self._scale_factor



_parameters = None

def get_parameters():
    global _parameters
    if _parameters is None:
        _parameters = Parameters()
    return _parameters
