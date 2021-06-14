from utils                                      import Utils
import mappers

class ParticipantMapper:
    @staticmethod
    def toDTO(participant):
        my_dto = dict()

        my_dto['sample_round']                  = mappers.SampleRoundMapper.toDTO(participant.sample_round)
        my_dto['subscription_date']             = Utils.to_iso_zulu(participant.subscription_date)

        return my_dto