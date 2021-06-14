from utils                              import Utils
import mappers

class SampleRoundMapper:
    @staticmethod
    def toDTO(sample_round):
        my_dto = dict()

        my_dto['name']                          = sample_round.name
        my_dto['sample_round_key']              = sample_round.sample_round_key
        my_dto['start_date']                    = Utils.to_iso_zulu(sample_round.start_date)
        my_dto['end_date']                      = Utils.to_iso_zulu(sample_round.end_date)

        my_dto['number_of_participants'] = len(sample_round.participants)
        return my_dto