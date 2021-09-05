package kr.ac.kpu.firstproject.ui
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import okhttp3.Call as CallOk
import okhttp3.Response as ResponseOk
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import kotlinx.android.synthetic.main.bottomsheet_fragment.*

import kr.ac.kpu.firstproject.R
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit

class BottomSheetFragment: BottomSheetDialogFragment() {

    val TAG = "TAG_MainActivity"
    lateinit var mRetrofit :Retrofit
    lateinit var mRetrofitAPI: RetrofitAPI
    lateinit var mCallResult : Call<Result>
    val result = "hello"
    var userEmail: String = "noNamed"
    var userText: String = "noNamed"

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.bottomsheet_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

        super.onViewCreated(view, savedInstanceState)
        setRetrofit()
        userEmail = arguments?.getString("user_email").toString()

        // android --> firebase : 데이터 전송
        request_button.setOnClickListener { // debug 필요한 구문
            userText = user_input.text.toString().trim()
            uploadFile()
        }
    }

    private fun uploadFile() {
        val mOkHttpClient = OkHttpClient.Builder()
            .connectTimeout(100, TimeUnit.SECONDS)
            .readTimeout(100, TimeUnit.SECONDS)
            .writeTimeout(100, TimeUnit.SECONDS)
            .build()

        val fileName = Environment.getExternalStorageDirectory().toString() +"/Download/myrec.m4a"
        Log.d("TAG",fileName)
        val requestBody = MultipartBody.Builder().setType(MultipartBody.FORM).addFormDataPart("user_email",userEmail)
            .addFormDataPart("file", "myrec.wav", File(fileName).asRequestBody("audio/wav".toMediaType()))
            .build()

        val request = Request.Builder().url("http://172.30.1.55:5000/predict").post(requestBody).build()

        val call = mOkHttpClient.newCall(request)

        Log.d("TAG", call.toString())

        call.enqueue(object : Callback {
            override fun onFailure(call: CallOk, e: IOException) {
                Log.d("TAG",e.toString())
            }

            override fun onResponse(call: CallOk, response: ResponseOk) {
                callResult()

            }
        })
    }

    // 리스트를 불러온다.
    private fun callResult() {
        mCallResult = mRetrofitAPI.getResult(result) //비어있을수도 있으니 앞에 초기값을 선언함
        mCallResult.enqueue(mRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    //http요청을 보냈고 이건 응답을 받을 콜벡메서드
    private val mRetrofitCallback  = (object : retrofit2.Callback<Result>{
        override fun onFailure(call: Call<Result>, t: Throwable) {
            t.printStackTrace()
        }

        override fun onResponse(call: Call<Result>, response: Response<Result>) {
            val result = response.body()
            Log.d(TAG, "결과는 => $result")
            Toast.makeText(context,"예측 결과: $result",Toast.LENGTH_SHORT).show()
        }
    })

    private fun setRetrofit(){
        //레트로핏으로 가져올 url설정하고 세팅
        mRetrofit = Retrofit
            .Builder()
            .baseUrl("http://172.30.1.55:5000")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        //인터페이스로 만든 레트로핏 api요청 받는 것 변수로 등록
        mRetrofitAPI = mRetrofit.create(RetrofitAPI::class.java)
    }

}