from spinnman.connections.udp_packet_connections import EIEIOConnection
from spinnman.messages.eieio.data_messages import EIEIODataMessage
from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
from spinn_utilities import conf_loader
import spynnaker.pyNN
from spinnman.messages.eieio.eieio_type import EIEIOType

config = conf_loader.load_config(
    spynnaker.pyNN, AbstractSpiNNakerCommon.CONFIG_FILE_NAME)

udp_connection = EIEIOConnection(
    remote_host=config.get("Machine", "machineName"), remote_port=12345)

key = 0x70800
# key = 0x800
payload = 1


message = EIEIODataMessage.create(EIEIOType.KEY_32_BIT)
message.add_key(key)
udp_connection.send_eieio_message(message)
