package com.example.kpu2021mk3

import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.Settings
import android.view.View
import android.widget.Toast
import androidx.annotation.Nullable
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_service.*
import java.lang.Exception
import java.util.*
import java.util.jar.Manifest
import kotlin.concurrent.timer

/* service
    stop watch
    record m4a
*/
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

//    private fun isPermissionGranted(): Boolean {
//        if(Build.VERSION.SDK_INT == Build.VERSION_CODES.R){
//            // For Android 11
//            return Environment.isExternalStorageManager()
//        } else{
//            // For Below
//            var readEnternalStoragePermission : Int = ContextCompat.checkSelfPermission(this, android.Manifest.permission.READ_EXTERNAL_STORAGE)
//            return readEnternalStoragePermission == PackageManager.PERMISSION_GRANTED
//        }
//    }
//    public fun takePermissions(view: View){
//        if (isPermissionGranted()){
//            Toast.makeText(this, "Permission Already Granted", Toast.LENGTH_SHORT).show()
//        }else{
//            takePermission()
//        }
//    }
//
//    private fun takePermission(){
//        if(Build.VERSION.SDK_INT == Build.VERSION_CODES.R) {
//            try{
//                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
//                intent.addCategory("android.intent.category.DEFAULT")
//                intent.setData(Uri.parse(String.format("package:%s",applicationContext.packageName)))
//                startActivityForResult(intent,100)
//            } catch(e : Exception){
//                intent = Intent()
//                intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
//                startActivityForResult(intent,100)
//            }
//        } else{
////            ActivityCompat.requestPermissions(this, {new String[] android.Manifest.permission.READ_EXTERNAL_STORAGE},101)  :: java
////            var StringArray = emptyArray<String>
//            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.READ_EXTERNAL_STORAGE),101)  // 임시
//        }
//    }
//
//    protected override fun onActivityResult(requestCode: Int, resultCode: Int, data:Intent?){
//        super.onActivityResult(requestCode, resultCode, data)
//        if(resultCode == RESULT_OK){
//            if(requestCode == 100){
//                if(Build.VERSION.SDK_INT == Build.VERSION_CODES.R){
//                    if(Environment.isExternalStorageManager()){
//                        Toast.makeText(this,"Permission Granted",Toast.LENGTH_SHORT).show()
//                    } else{
//                        takePermission()
//                    }
//                }
//            }
//        }
//    }
////    public override fun onRequestPermissionsResult(requestCode: Int, @NonNull String[] permissions, @NonNull int[] grantResults){  :: java
//    public override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray){
//        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
//            if(grantResults.isNotEmpty()){
//                if(requestCode == 101){
//                    var readExternalStorage : Boolean = grantResults[0] == PackageManager.PERMISSION_GRANTED
//                    if(readExternalStorage){
//                        Toast.makeText(this, "Read Permission is Granted in andriod 10 or below", Toast.LENGTH_SHORT).show()
//                    } else{
//                        takePermission()
//                    }
//                }
//            }
//    }


    // 3번째 4번째 방안이 도움됨
    // https://www.youtube.com/watch?v=_IbfUJS13h8&ab_channel=MickeyFaisal :: permission 참조중 --> 13분대까지 진행함 --> 실패
    // https://itandhumanities.tistory.com/2 :: kotlin 배열 사용법
    // https://stackoverflow.com/questions/44239869/whats-the-kotlin-equivalent-of-javas-string :: 3번째 방안 낙찰
    // https://kookyungmin.github.io/language/2018/05/22/java_06/ :: java string
    // https://stackoverflow.com/questions/23527767/open-failed-eacces-permission-denied :: sdk 등을 29로 변경

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

        if(ActivityCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO)!= PackageManager.PERMISSION_GRANTED) {//권한을 요청하고 요청이 수행이 되면 그 button이 활성화가 되는 것을 의미하는 함수
            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.RECORD_AUDIO,android.Manifest.permission.WRITE_EXTERNAL_STORAGE),111)
            start_button.isEnabled = true }

        //스타트 버튼 클릭
        start_button.setOnClickListener{
            mr.setAudioSource(MediaRecorder.AudioSource.MIC)
            mr.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4) //저장할 파일의 확장자를 정해주는 것
            mr.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB)
            mr.setAudioEncodingBitRate(16*44100)  // high quality
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