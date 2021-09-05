package kr.ac.kpu.firstproject.ui

import retrofit2.http.GET
import retrofit2.Call
import retrofit2.http.Query

interface RetrofitAPI {
    @GET("/predict")//서버에 GET요청을 할 주소를 입력
    fun getResult(@Query("result") result: String): Call<Result>
}
