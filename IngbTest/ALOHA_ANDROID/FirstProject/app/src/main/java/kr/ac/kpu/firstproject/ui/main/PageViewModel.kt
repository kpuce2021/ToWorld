package kr.ac.kpu.firstproject.ui.main

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.Transformations
import androidx.lifecycle.ViewModel

class PageViewModel:ViewModel() {

    val _index = MutableLiveData<Int>()
    val maintext: LiveData<String> = Transformations.map(_index) // 라이브 데이터는 이름처럼 실시간으로 바뀌는 것을 수행해준대
    {
        ""
    }

    val subtext: LiveData<String> = Transformations.map(_index){
        ""
    }

    fun setIndex(index: Int){
        _index.value = index
    }
}