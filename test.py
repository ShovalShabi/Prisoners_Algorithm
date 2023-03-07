from Prisoners_Algorithm.model_manger import ModelManger

model_mngr= ModelManger(10,1000,None)

model_mngr.run_threads()
#print(model_mngr.dict_rounds)


for round in range(model_mngr.num_rounds):
    print(model_mngr.dict_rounds[round+1])