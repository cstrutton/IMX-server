from pylogix import PLC

with PLC() as comm:
    comm.ProcessorSlot = 3
    comm.IPAddress = '10.4.42.135'
    result = comm.Read('Batch_Data.Remaining')
    print(result)
