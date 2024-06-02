from test_dvs_printf import listfunction
import torch as pt 

pt_list = pt.tensor([
    [[1,1,1],[2,2,2],[3,3,3]],
    [[4,4,4],[5,5,5],[6,6,6]],
    [[7,7,7],[8,8,8],[9,9,9]], 
],dtype=pt.int64)

def test_arrayToList_tf():
    assert listfunction((pt_list,))==[
'tensor([[[1, 1, 1],', '         [2, 2, 2],', '         [3, 3, 3]],', '', 
'        [[4, 4, 4],', '         [5, 5, 5],', '         [6, 6, 6]],', '', 
'        [[7, 7, 7],', '         [8, 8, 8],', '         [9, 9, 9]]])']

test_pt_list=[
 '[1, 1, 1]', '[2, 2, 2]', '[3, 3, 3]', 
 '[4, 4, 4]', '[5, 5, 5]', '[6, 6, 6]', 
 '[7, 7, 7]', '[8, 8, 8]', '[9, 9, 9]']

def test_getmat_true_pt():
    assert listfunction((pt_list,),getmat= True )==test_pt_list
    assert listfunction((pt_list,),getmat="true")==test_pt_list

def test_getmat_show_tf():
    assert listfunction((pt_list,),getmat="true show info")==test_pt_list + \
["<class 'torch.Tensor'", ' dtype=torch.int64 ', ' shape=torch.Size([3, 3, 3])>']

