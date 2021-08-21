package com.example.kpu2021mk3
import android.app.ProgressDialog
import android.content.ContentValues.TAG
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.text.InputFilter
import android.text.Spanned
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.firebase.database.*
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.FirebaseStorage
import kotlinx.android.synthetic.main.bottomsheet_fragment.*
import java.io.File
import java.util.regex.Pattern

// 학습모드!!

class BottomSheetFragment() : BottomSheetDialogFragment() {

    var userId: String = "noNamed"
    var userEmail: String = "noNamed"
    var fileNum: Int = 0 // file numbering
    var userText: String = "noNamed"

    var fileName: String = "noNamed"

    // private lateinit var database: DatabaseReference //firebase realtime DB 사용
    private val database = Firebase.database.reference

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.bottomsheet_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

        super.onViewCreated(view, savedInstanceState)

        userEmail = arguments?.getString("user_email").toString()
        userEmail = userEmail.split(".")[0]
//        userId= arguments?.getString("user_id").toString()

        // android --> firebase : 데이터 전송
        select_button.setOnClickListener { // debug 필요한 구문

            userText = user_input.text.toString().trim()

            Log.w(TAG, "click button : "+userText)
            uploadData()
            checkRealtimeDB()
            textView.text = "정답"
        }
    }

    //debug
    fun checkMeta(){  // metadata check

    }
    
    /*
        upload data에서 userId, userId - fileName - checkKey : True setting
        
        checkRealtimeDB에서 userId - fileName - checkKey : True일 경우 False setting으로 2회차 막음
     */

    fun uploadData(){ //realtime DB
        Log.w(TAG, "uploadData : "+userText)
        fileName = userText
        database.child(userEmail).child("userId").setValue(userEmail+".com")
        database.child(userEmail).child(fileName).child("checkKey").setValue("true")
//        database.child(userEmail).child("userId").setValue(userEmail)
//        database.child(userEmail).child(fileName).child("checkKey").setValue("true")
//        database.child(userId).child(fileName).child("fileName").setValue(fileName+".m4a")
    }

    fun checkRealtimeDB(){
        val realtimeDBEvent = object : ValueEventListener { // 이벤트성
            override fun onDataChange(snapshot: DataSnapshot) {
                var previous_number:Int = 0

                // 숫자 체크 코드
                // filename - check key : true 일 경우
                // userId --> userEmail
                if(snapshot.child(userEmail).child(fileName).child("checkKey").getValue().toString().equals("true")){  //추후에 변경할 예정임.
                    Log.w(TAG, "on data change entrance if : "+userText)
                    Log.w(TAG, "on data change entrance : "+snapshot.child(userId).child(fileName))

                    if(snapshot.child(userEmail).child(fileName).child("number").exists()){
                        previous_number = snapshot.child(userEmail).child(fileName).child("number").getValue().toString().toInt() + 1 }
                    else{
                        previous_number = 0 }
                    Log.w(TAG, "on data change entrance : "+snapshot.child(userEmail).child(fileName).child("number"))
                    Log.w(TAG, "on data change entrance : ")

                    database.child(userEmail).child(fileName).child("checkKey").setValue("false")
//                    database.child(userId).child(fileName).child("number").setValue(userEmail+"/"+fileName+previous_number+".m4a")  // input type error
                    database.child(userEmail).child(fileName).child("number").setValue(previous_number)  // 변경 포인트

                    uploadFile(previous_number)
                }
                else{
                    Log.w(TAG, "realtimeDB value error : checkKey maybe false")
                }
            }
            override fun onCancelled(error: DatabaseError) {
                Log.w(TAG, "loadPost:onCancelled", error.toException())
            }
        }

        database.addListenerForSingleValueEvent(realtimeDBEvent)
    }


    fun uploadFile(fileNumber:Int) { // storage
        Log.w(TAG, "uploadFile : "+userText)
        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/my_audio_file.m4a" //파일의 저장 위치
        val fileUri = Uri.fromFile(File(path))

        if(fileUri!=null){
            var pd = ProgressDialog(context)
            pd.setTitle("업로딩 중")
            pd.show()

            var mediaRef = FirebaseStorage.getInstance().reference.child("audio").child(userEmail+".com").child(fileName).child(fileName+fileNumber+ ".m4a")
            mediaRef.putFile(fileUri)
                    .addOnSuccessListener { p0 ->
                        pd.dismiss()
                        Toast.makeText(context, "파일 업로드", Toast.LENGTH_LONG).show()
                    }
                    .addOnFailureListener{ p0->
                        pd.dismiss()
                        Toast.makeText(context, p0.message, Toast.LENGTH_LONG).show()
                    }
                    .addOnProgressListener { p0 ->
                        var progress =  (100.0 * p0.bytesTransferred) / p0.totalByteCount
                        pd.setMessage("업로드 됨 ${progress.toInt()} %")
                    }
        }
    }
}