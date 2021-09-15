package kr.ac.kpu.firstproject.ui

import android.content.ContentValues.TAG
import android.content.Intent
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.Gravity
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.drawerlayout.widget.DrawerLayout
import com.google.android.material.navigation.NavigationView
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_main.main_action_menu
import kotlinx.android.synthetic.main.activity_main.main_drawer_layout
import kotlinx.android.synthetic.main.activity_main.main_navigation_view
import kotlinx.android.synthetic.main.activity_main.main_toolbar
import kotlinx.android.synthetic.main.activity_main.milliTextView
import kotlinx.android.synthetic.main.activity_main.secTextView
import kotlinx.android.synthetic.main.activity_main.start_button
import kotlinx.android.synthetic.main.activity_main.stop_button
import kotlinx.android.synthetic.main.activity_using.*
import kr.ac.kpu.firstproject.R
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query
import java.io.File
import java.io.IOException
import java.util.*
import java.util.concurrent.TimeUnit
import kotlin.concurrent.timer

class UsingActivity : AppCompatActivity(), NavigationView.OnNavigationItemSelectedListener {

    companion object {
        private var mr: MediaRecorder = MediaRecorder()
        private var time = 0
        private var timetask: Timer? = null
        lateinit var mRetrofit: Retrofit
        lateinit var mRetrofitAPI: RetrofitAPI
        lateinit var mCallResult: Call<Result>
        val result = "default"
        var userEmail: String = "default"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_using)
        setSupportActionBar(main_toolbar)
        setRetrofit()

        userEmail =  intent.getStringExtra("user_email").toString()
        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.m4a" //파일의 저장 위치

        main_drawer_layout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED)
        main_navigation_view.setNavigationItemSelectedListener(this)

        stop_button.isEnabled = false
        start_button.isEnabled = true

        //스타트 버튼 클릭
        start_button.setOnClickListener{
            mr.setAudioSource(MediaRecorder.AudioSource.MIC)
            mr.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            mr.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB)
            mr.setAudioEncodingBitRate(16 * 44100)
            mr.setAudioSamplingRate(44100)
            mr.setOutputFile(path)
            mr.prepare()
            mr.start()

            time_start() // timer start
            stop_button.isEnabled = true
            start_button.isEnabled = false
        }

        //정지 버튼 클릭
        stop_button.setOnClickListener{
            mr.stop()
            time_reset() // timer reset
            start_button.isEnabled = true //정지가 눌리면 시작버튼은 비활성화
            stop_button.isEnabled = false
            uploadFile()
        }

        main_action_menu.setOnClickListener{
            main_drawer_layout.openDrawer(Gravity.LEFT)
        }
    }

    private fun uploadFile() {
        val mOkHttpClient = OkHttpClient.Builder()
                .connectTimeout(100, TimeUnit.SECONDS)
                .readTimeout(100, TimeUnit.SECONDS)
                .writeTimeout(100, TimeUnit.SECONDS)
                .build()

        val fileName = Environment.getExternalStorageDirectory().toString() +"/Download/myrec.m4a"
        val requestBody = MultipartBody.Builder().setType(MultipartBody.FORM).addFormDataPart("user_email",userEmail)
                .addFormDataPart("file", "myrec.wav", File(fileName).asRequestBody("audio/wav".toMediaType()))
                .build()

        val request = Request.Builder().url("http://192.168.219.101:5000/predict").post(requestBody).build()
        val call = mOkHttpClient.newCall(request)

        call.enqueue(object : Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
            }

            override fun onResponse(call: okhttp3.Call, response: Response) {
                callResult()
            }
        })
    }

    private fun callResult() {
        mCallResult = mRetrofitAPI.getResult(result) //비어있을수도 있으니 앞에 초기값을 선언함
        mCallResult.enqueue(mRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    //http 요청을 보냈고 이건 응답을 받을 콜벡메서드
    private val mRetrofitCallback  = (object : retrofit2.Callback<Result>{
        override fun onFailure(call: Call<Result>, t: Throwable) {
            t.printStackTrace()
        }

        override fun onResponse(call: Call<Result>, response: retrofit2.Response<Result>) {
            val result = response.body()
            Log.d(TAG, "결과는 => $result")
            getResultText.text = "$result"
        }
    })


    private fun setRetrofit(){
        //레트로핏으로 가져올 url 설정하고 세팅
        mRetrofit = Retrofit
                .Builder()
                .baseUrl("http://192.168.219.101:5000")
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        //인터페이스로 만든 레트로핏 api 요청 받는 것 변수로 등록
        mRetrofitAPI = mRetrofit.create(RetrofitAPI::class.java)
    }


    // 타이머
    private fun time_start(){
        timetask = timer(period = 10){
            time++  // time 변수 1씩 증가
            val sec = time / 100
            val milli = time % 100

            runOnUiThread{  // UI 갱신
                secTextView.text = "$sec"
                milliTextView.text = "$milli"
            }
        }
    }

    private fun time_reset(){
        timetask?.cancel()
        time = 0
        secTextView.text = "0"
        milliTextView.text = "00"
    }

    override fun onNavigationItemSelected(item: MenuItem): Boolean {
        when(item.itemId) {
            R.id.action_using_mode -> {
                main_drawer_layout.closeDrawer(Gravity.LEFT)
                val intent = Intent(applicationContext, MainActivity::class.java)
                intent.putExtra("user_email", userEmail)
                startActivity(intent)
            }
            R.id.action_logout -> {
                main_drawer_layout.closeDrawer(Gravity.LEFT)
                FirebaseAuth.getInstance().signOut()
                startActivity(Intent(this@UsingActivity, LoginActivity::class.java))
                finish()
            }
        }
        return true
    }
}

interface RetrofitAPI {
    @GET("/predict")//서버에 GET요청을 할 주소를 입력
    fun getResult(@Query("result") result: String): Call<Result>
}