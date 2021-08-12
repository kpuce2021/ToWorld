package kr.ac.kpu.firstproject.ui

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
import kotlinx.android.synthetic.main.activity_main.*
import kr.ac.kpu.firstproject.R
import java.util.*
import kotlin.concurrent.timer

class MainActivity : AppCompatActivity(), NavigationView.OnNavigationItemSelectedListener {

    lateinit var mr: MediaRecorder
    private var time = 0
    private var timetask: Timer? = null

    var userEmail: String = "noNamed"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(main_toolbar)

        userEmail =  intent.getStringExtra("user_email").toString()

        Log.d("TAG",userEmail)

        main_drawer_layout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED)
        main_navigation_view.setNavigationItemSelectedListener(this)

        val bottomSheetFragment = BottomSheetFragment()

        log_out_button.setOnClickListener{
            FirebaseAuth.getInstance().signOut()
            startActivity(Intent(this@MainActivity, LoginActivity::class.java))
            finish()
        }

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.m4a" //파일의 저장 위치

        mr = MediaRecorder()
        start_button.isEnabled = false
        stop_button.isEnabled = false

        if(ActivityCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO)!= PackageManager.PERMISSION_GRANTED) //권한을 요청하고 요청이 수행이 되면 그 button이 활성화가 되는 것을 의미하는 함수
            ActivityCompat.requestPermissions(
                this, arrayOf(
                    android.Manifest.permission.RECORD_AUDIO,
                    android.Manifest.permission.WRITE_EXTERNAL_STORAGE
                ), 111
            )

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

            time_reset() // timer reset
            start_button.isEnabled = true //정지가 눌리면 시작버튼은 비활성화

            val bundle = Bundle()
            bundle.putString("user_email", userEmail)

            bottomSheetFragment.arguments = bundle
            bottomSheetFragment.show(supportFragmentManager, "BottomSheetDialog")
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
            // 아이템에 있는 것을 클릭하게 되면
            R.id.action_create_tournament -> {
                main_drawer_layout.closeDrawer(Gravity.LEFT)
                val intent = Intent(applicationContext, TournamentCreatePopupActivity::class.java)
                startActivity(intent)
                // Intent로 연결 하지만 아직 등록은 차후에 구현 (1)
            }

            //내가 만든 토너먼트? list 확인인가?
            R.id.action_my_create_tournament -> {
                main_drawer_layout.closeDrawer(Gravity.LEFT)
            }
        }
        return true
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if(requestCode==111 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
            start_button.isEnabled = true
    }
}