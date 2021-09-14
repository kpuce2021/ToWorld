package kr.ac.kpu.firstproject.ui
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.DialogFragment
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
import retrofit2.http.GET
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit

class BottomSheetFragment: BottomSheetDialogFragment(),BottomDialogAdapter.OnItemClickListener {

    companion object {
        lateinit var mRetrofit: Retrofit
        lateinit var mRetrofitAPI: CNN_API
        lateinit var oRetrofitAPI: CNN_OPER
        lateinit var mCallResult: Call<CNN_Result>
        val res = "default"
        val time = "default"
        var userEmail: String = "default"
        var item = mutableListOf<CNN_Result>()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.bottomsheet_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        userEmail = arguments?.getString("user_email").toString()
        user_input.visibility = View.GONE
        request_button.visibility = View.GONE
        setRetrofit()
        predictFile()

         no_answer_tv.setOnClickListener { // debug 필요한 구문
             user_input.visibility = View.VISIBLE
             request_button.visibility = View.VISIBLE
             recyclerView.visibility = View.GONE
             close_button.visibility = View.GONE
             no_answer_tv.visibility = View.GONE
        }

        close_button.setOnClickListener{
            dismiss()
        }

        request_button.setOnClickListener{
            uploadFile(user_input.text.toString().trim())
            Toast.makeText(context,"업로드가 완료되었습니다.",Toast.LENGTH_SHORT).show()
        }
    }

    private fun predictFile() {
        val mOkHttpClient = OkHttpClient.Builder()
            .connectTimeout(100, TimeUnit.SECONDS)
            .readTimeout(100, TimeUnit.SECONDS)
            .writeTimeout(100, TimeUnit.SECONDS)
            .build()

        val requestBody = MultipartBody.Builder().setType(MultipartBody.FORM).addFormDataPart("user_email",userEmail)
            .build()

        val request = Request.Builder().url("http://192.168.219.100:5000/pre_con").post(requestBody).build()
        val call = mOkHttpClient.newCall(request)

        call.enqueue(object : Callback {
            override fun onFailure(call: CallOk, e: IOException) {
                Log.d("TAG",e.toString())
            }

            override fun onResponse(call: CallOk, response: ResponseOk) {
                callResult()
            }
        })
    }

    private fun uploadFile(selectedItem:String) {
        val mOkHttpClient = OkHttpClient.Builder()
            .connectTimeout(100, TimeUnit.SECONDS)
            .readTimeout(100, TimeUnit.SECONDS)
            .writeTimeout(100, TimeUnit.SECONDS)
            .build()

        val fileName = Environment.getExternalStorageDirectory().toString() +"/Download/myrec.m4a"
        val requestBody = MultipartBody.Builder().setType(MultipartBody.FORM).addFormDataPart("user_email",userEmail)
            .addFormDataPart("answer", selectedItem)
            .addFormDataPart("file", "myrec.wav", File(fileName).asRequestBody("audio/wav".toMediaType()))
            .build()

        val request = Request.Builder().url("http://192.168.219.100:5000/con").post(requestBody).build()
        val call = mOkHttpClient.newCall(request)

        call.enqueue(object : Callback {
            override fun onFailure(call: CallOk, e: IOException) {
                Log.d("TAG",e.toString())
            }

            override fun onResponse(call: CallOk, response: ResponseOk) {
                ocallResult()
            }
        })
    }

    // 리스트를 불러온다.
    private fun callResult() {
        mRetrofitAPI.fetchAllitem().enqueue(mRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    private fun ocallResult() {
        oRetrofitAPI.fetchAllitem().enqueue(mRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    //http요청을 보냈고 이건 응답을 받을 콜벡메서드
    private val mRetrofitCallback  = (object : retrofit2.Callback<List<CNN_Result>>{
        override fun onFailure(call: Call<List<CNN_Result>>, t: Throwable) {
            t.printStackTrace()
        }

        override fun onResponse(call: Call<List<CNN_Result>>, response: Response<List<CNN_Result>>) {
            showData(response.body()!!)
            item = (response.body() as MutableList<CNN_Result>?)!!
        }
    })

    private fun setRetrofit(){
        mRetrofit = Retrofit
            .Builder()
            .baseUrl("http://192.168.219.100:5000")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        mRetrofitAPI = mRetrofit.create(CNN_API::class.java)
        oRetrofitAPI = mRetrofit.create(CNN_OPER::class.java)
    }

    private fun showData(item: List<CNN_Result>){
        recyclerView.apply{
            adapter = BottomDialogAdapter(item,this@BottomSheetFragment)
        }
    }

    override fun onItemClick(position: Int) {
        Toast.makeText(context,"Item" + item[position] + "clicked", Toast.LENGTH_SHORT).show()
        val clickedItem:CNN_Result = item[position]
        Log.d("TAG",clickedItem.toString())
        uploadFile(clickedItem.result)
        // 예측한 정답 중 하나의 데이터를 다시 보낸 다음 response로...업데이트 된 것을 다시 받아오면 되겠다. count가 증가하니까
    }
}

// predict 이름을 이렇게 만들어버렸음...
interface CNN_API {
    @GET("/pre_con")//서버에 GET요청을 할 주소를 입력
    // fun getResult(@Query("result") result: String, @Query("count") count: String): Call<List<Cnn_Result>>
    fun fetchAllitem(): Call<List<CNN_Result>>
}

interface CNN_OPER{
    @GET("/con")
    fun fetchAllitem(): Call<List<CNN_Result>>
}