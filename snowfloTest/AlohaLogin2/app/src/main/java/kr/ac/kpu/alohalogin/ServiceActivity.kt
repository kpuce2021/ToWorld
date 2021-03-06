package kr.ac.kpu.alohalogin
import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import androidx.core.app.ActivityCompat
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_service.*

// record audio, send data fragment

// test용 BlankFragment 있음 -> 지울것.
open class ServiceActivity : AppCompatActivity() {
    lateinit var mr: MediaRecorder
    var userId: String = "noNamed"
    var userEmail: String = "noNamed"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_service)

        userId = intent.getStringExtra("user_id").toString()
        userEmail =  intent.getStringExtra("user_email").toString()

        val bottomSheetFragment = BottomSheetFragment()
        val blankFragment = BlankFragment() // test용 BlankFragment

        log_out_button.setOnClickListener{
            FirebaseAuth.getInstance().signOut()
            startActivity(Intent(this@ServiceActivity,MainActivity::class.java))
            finish()
        }

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.3gp" //안드로이드내 파일 저장 위치
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
            mr.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP) //저장할 파일의 확장자를 정해주는 것
            mr.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB)
            mr.setOutputFile(path)
            mr.prepare()
            mr.start()
            stop_button.isEnabled = true
            start_button.isEnabled = false

        }

        //정지 버튼 클릭
        stop_button.setOnClickListener{
            mr.stop()
            start_button.isEnabled = true //정지가 눌리면 시작버튼은 비활성화
            stop_button.isEnabled = false

            var dataBundle = Bundle()
            dataBundle.putString("user_id", userId)
            dataBundle.putString("user_email", userEmail)


            //bottomSheetFragment.onCreateDialog(bundle)
            /*
            bottomSheetFragment.show(supportFragmentManager, "BottomSheetDialog")
            bottomSheetFragment.setArguments(dataBundle)
            */

            blankFragment.show(supportFragmentManager, "BottomSheetDialog")
            blankFragment.setArguments(dataBundle)

        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if(requestCode==111 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
            start_button.isEnabled = true
    }
}