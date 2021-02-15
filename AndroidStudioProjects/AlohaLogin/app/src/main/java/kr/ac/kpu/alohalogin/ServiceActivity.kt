package kr.ac.kpu.alohalogin
import android.app.ProgressDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.net.Uri
import android.net.Uri.fromFile
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.widget.Toast
import androidx.core.app.ActivityCompat
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.storage.FirebaseStorage
import kotlinx.android.synthetic.main.activity_service.*
import java.io.File

class ServiceActivity : AppCompatActivity() {
    lateinit var mr: MediaRecorder
    lateinit var filepath: Uri

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_service)

        //val userId = intent.getStringExtra("user_id")

        log_out_button.setOnClickListener{
            FirebaseAuth.getInstance().signOut()
            startActivity(Intent(this@ServiceActivity,MainActivity::class.java))
            finish()
        }

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.3gp" //파일의 저장 위치
        val fileUri = fromFile(File(path))

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

            filepath = fileUri
            uploadFile()

        }


    }
    private fun uploadFile() {

        if(filepath!=null){
            var pd = ProgressDialog(this)
            pd.setTitle("업로딩 중")
            pd.show()

            var mediaRef = FirebaseStorage.getInstance().reference.child("user/record.3gp")
            mediaRef.putFile(filepath)
                .addOnSuccessListener { p0 ->
                    pd.dismiss()
                    Toast.makeText(applicationContext, "파일 업로드", Toast.LENGTH_LONG).show()

                }

                .addOnFailureListener{ p0->
                    pd.dismiss()
                    Toast.makeText(applicationContext, p0.message, Toast.LENGTH_LONG).show()

                }
                .addOnProgressListener { p0 ->
                    var progress =  (100.0 * p0.bytesTransferred) / p0.totalByteCount
                    pd.setMessage("업로드 됨 ${progress.toInt()} %")
                }
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if(requestCode==111 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
            start_button.isEnabled = true
    }
}