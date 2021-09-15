package kr.ac.kpu.firstproject.ui

import android.animation.ObjectAnimator
import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.Gravity
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.drawerlayout.widget.DrawerLayout
import com.google.android.material.navigation.NavigationView
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_login.*
import kotlinx.android.synthetic.main.activity_main.*
import kr.ac.kpu.firstproject.R
import okhttp3.*
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query
import java.io.IOException
import java.util.*
import java.util.concurrent.TimeUnit
import kotlin.concurrent.timer

class MainActivity : AppCompatActivity(), NavigationView.OnNavigationItemSelectedListener {

    companion object{
        private var mr: MediaRecorder = MediaRecorder()
        private var time = 0
        private var timetask: Timer? = null
        var userEmail: String = "noNamed"
        lateinit var pRetrofit: Retrofit
        lateinit var pRetrofitAPI: CNN_Progress
        lateinit var pCallResult: Call<Result>
        val result = "0"
        private var current_percent = 0

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(main_toolbar)

        val bottomDialogFragment = BottomSheetFragment()

        userEmail = intent.getStringExtra("user_email").toString()

        main_drawer_layout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED)
        main_navigation_view.setNavigationItemSelectedListener(this)

        if(ActivityCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO)!= PackageManager.PERMISSION_GRANTED)
            ActivityCompat.requestPermissions(
                    this, arrayOf(
                    android.Manifest.permission.RECORD_AUDIO,
                    android.Manifest.permission.WRITE_EXTERNAL_STORAGE
            ), 111
            )

        setRetrofit()

        

        val mOkHttpClient = OkHttpClient.Builder()
                .connectTimeout(100, TimeUnit.SECONDS)
                .readTimeout(100, TimeUnit.SECONDS)
                .writeTimeout(100, TimeUnit.SECONDS)
                .build()

        val requestBody = MultipartBody.Builder().setType(MultipartBody.FORM).addFormDataPart("user_email", userEmail).build()

        val request = Request.Builder().url("http://192.168.219.101:5000/progress").post(requestBody).build()
        val call = mOkHttpClient.newCall(request)

        call.enqueue(object : Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
            }

            override fun onResponse(call: okhttp3.Call, response: Response) {
                callResult()
            }
        })

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.m4a" //파일의 저장 위치

        stop_button.isEnabled = false
        start_button.isEnabled = true

        //스타트 버튼 클릭
        start_button.setOnClickListener{
            mr.setAudioSource(MediaRecorder.AudioSource.MIC)
            mr.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4) //저장할 파일의 확장자를 정해주는 것
            mr.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB)
            mr.setAudioEncodingBitRate(16 * 44100)  // high quality
            mr.setAudioSamplingRate(44100)  // high quality
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
            time_reset()
            start_button.isEnabled = true //정지가 눌리면 시작버튼은 비활성화

            val bundle = Bundle()
            bundle.putString("user_email", userEmail)
            bottomDialogFragment.arguments = bundle
            bottomDialogFragment.show(supportFragmentManager, "BottomSheetDialog")

            stop_button.isEnabled = false
        }

        main_action_menu.setOnClickListener{
            main_drawer_layout.openDrawer(Gravity.LEFT)
        }
    }

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
                val intent = Intent(applicationContext, UsingActivity::class.java)
                intent.putExtra("user_email", userEmail)
                startActivity(intent)
            }
            R.id.action_logout -> {
                main_drawer_layout.closeDrawer(Gravity.LEFT)
                FirebaseAuth.getInstance().signOut()
                startActivity(Intent(this@MainActivity, LoginActivity::class.java))
                finish()
            }
        }
        return true
    }

    //progress 설정
    private fun setRetrofit(){
        //레트로핏으로 가져올 url 설정하고 세팅
        pRetrofit = Retrofit
                .Builder()
                .baseUrl("http://192.168.219.101:5000")
                .addConverterFactory(GsonConverterFactory.create())
                .build()

        //인터페이스로 만든 레트로핏 api 요청 받는 것 변수로 등록
        pRetrofitAPI = pRetrofit.create(CNN_Progress::class.java)
    }

    private fun callResult() {
        pCallResult = pRetrofitAPI.getResult(result) //비어있을수도 있으니 앞에 초기값을 선언함
        pCallResult.enqueue(pRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    private val pRetrofitCallback  = (object : retrofit2.Callback<Result>{
        override fun onFailure(call: Call<Result>, t: Throwable) {
            t.printStackTrace()
        }
        override fun onResponse(call: Call<Result>, response: retrofit2.Response<Result>) {
            val count = response.body()
            var currentProgress = (count?.result?.toInt()?.times(10))
            if (count != null) {
                if (currentProgress != null) {
                    ObjectAnimator.ofInt(progress_bar, "progress", currentProgress)
                            .setDuration(800).start()

                    Log.d("TAG",(count?.result?.toInt()).toString())
                    current_percent = (count?.result?.toInt().times(100) / 20)
                    percent_cnn.text = "$current_percent%"
                }
            }
        }
    })
}

interface CNN_Progress{
    @GET("/progress")
    fun getResult(@Query("result") result: String): Call<Result>
}