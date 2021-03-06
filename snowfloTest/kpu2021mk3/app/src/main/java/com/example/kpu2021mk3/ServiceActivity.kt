package com.example.kpu2021mk3

import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import androidx.core.app.ActivityCompat
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_service.*
import java.util.*
import kotlin.concurrent.timer

class ServiceActivity : AppCompatActivity() {
    lateinit var mr: MediaRecorder
    var userId: String = "noNamed"
    var userEmail: String = "noNamed"

    private var time = 0
    private var timetask: Timer? = null
    
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_service)

        userId = intent.getStringExtra("user_id").toString()
        userEmail =  intent.getStringExtra("user_email").toString()

        val bottomSheetFragment = BottomSheetFragment()

        log_out_button.setOnClickListener{
            FirebaseAuth.getInstance().signOut()
            startActivity(Intent(this@ServiceActivity,MainActivity::class.java))
            finish()
        }

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/my_audio_file.m4a" //파일의 저장 위치
        //val fileUri = fromFile(File(path))

        mr = MediaRecorder()
        start_button.isEnabled = false
        stop_button.isEnabled = false

        if(ActivityCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO)!= PackageManager.PERMISSION_GRANTED) //권한을 요청하고 요청이 수행이 되면 그 button이 활성화가 되는 것을 의미하는 함수
            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.RECORD_AUDIO,android.Manifest.permission.WRITE_EXTERNAL_STORAGE),111)

        start_button.isEnabled = true

        //스타트 버튼 클릭
        start_button.setOnClickListener{
            mr.setAudioSource(MediaRecorder.AudioSource.MIC)
            mr.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4) //저장할 파일의 확장자를 정해주는 것
            mr.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB)
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

            val bundle = Bundle()
            bundle.putString("user_email", userEmail)
            bundle.putString("user_id", userId)

            bottomSheetFragment.arguments = bundle
            bottomSheetFragment.show(supportFragmentManager, "BottomSheetDialog")
            stop_button.isEnabled = false
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if(requestCode==111 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
            start_button.isEnabled = true
    }
}