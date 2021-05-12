package com.example.myapplication

import android.app.ProgressDialog
import android.content.ContentValues.TAG
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.text.InputFilter
import android.text.Spanned
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.ValueEventListener
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.FirebaseStorage
import kotlinx.android.synthetic.main.fragment_blank.*
import java.io.File
import java.util.regex.Pattern

/**
 * A simple [Fragment] subclass.
 * Use the [BlankFragment.newInstance] factory method to
 * create an instance of this fragment.
 */

// BottomSheetFragment == BlankFragment
class BlankFragment : BottomSheetDialogFragment() {

    var userId: String = "noNamed"
    var userEmail: String = "noNamed"
    var fileNum: Int = 0 // file numbering
    var userText: String = "noNamed"

    var fileName: String = "noNamed"

    // private lateinit var database: DatabaseReference //firebase realtime DB 사용
    private val database = Firebase.database.reference

    // fragment
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_blank, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

        super.onViewCreated(view, savedInstanceState)

        var textFilter = Array<InputFilter>(1,{ValidateFilter(50)})
        //user_input.filters = textFilter

        userEmail = arguments?.getString("user_email").toString()
        userId= arguments?.getString("user_id").toString()
        
        // 파일명 입력후 클릭함
        select_button.setOnClickListener { // debug 필요한 구문

            userText = user_input.text.toString().trim()

            Log.w(TAG, "click button : "+userText)
            uploadData()
            checkRealtimeDB()
        }
    }

    fun uploadData(){  // realtime DB
        Log.w(TAG, "uploadData : "+userText)
        fileName = userText
        database.child(userId).child("userId").setValue(userEmail)
        database.child(userId).child(fileName).child("checkKey").setValue("true")
    }

    fun checkRealtimeDB(){  // 1번 제한
        val realtimeDBEvent = object : ValueEventListener { // 이벤트성
            override fun onDataChange(snapshot: DataSnapshot) {
                var previous_number:Int = 0

                // 숫자 체크 코드
                if(snapshot.child(userId).child(fileName).child("checkKey").getValue().toString().equals("true")){  //추후에 변경할 예정임.
                    Log.w(TAG, "on data change entrance if : "+userText)
                    Log.w(TAG, "on data change entrance : "+snapshot.child(userId).child(fileName))

                    if(snapshot.child(userId).child(fileName).child("number").exists()){
                        previous_number = snapshot.child(userId).child(fileName).child("number").getValue().toString().toInt() + 1 }
                    else{
                        previous_number = 0 }
                    Log.w(TAG, "on data change entrance : "+snapshot.child(userId).child(fileName).child("number"))
                    Log.w(TAG, "on data change entrance : ")

                    database.child(userId).child(fileName).child("checkKey").setValue("false")
                    database.child(userId).child(fileName).child("number").setValue(previous_number)
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


    fun uploadFile(fileNumber:Int) {  // cloud storage
        Log.w(TAG, "uploadFile : "+userText)
        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.3gp" //파일의 저장 위치
        val fileUri = Uri.fromFile(File(path))

        if(fileUri!=null){
            var pd = ProgressDialog(context)
            pd.setTitle("업로딩 중")
            pd.show()

            var mediaRef = FirebaseStorage.getInstance().reference.child("audio").child(userEmail).child(fileName).child(fileName+fileNumber)
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

    inner class ValidateFilter(max:Int) : InputFilter {
        internal var mPattern: Pattern
        internal var mMax:Int = 0

        init{
            mPattern = Pattern.compile("[가-힣ㄱ-ㅎㅏ-ㅣ]")
            mMax = max
        }

        override fun filter(source: CharSequence, start: Int, end: Int, dest: Spanned?, dstart: Int, dend: Int): CharSequence? {
            val matcher = mPattern.matcher(source)
            if(!matcher.matches()){
                return ""
            } else {
                var keep = mMax - (dest!!.length - (dend - dstart))
                if(keep <= 0){
                    return ""
                } else if (keep >= end - start) {
                    return null
                } else {
                    keep += start
                    if(Character.isHighSurrogate(source[keep - 1])){
                        --keep
                        if(keep == start) {
                            return ""
                        }
                    }
                    return source.subSequence(start,keep)
                }
            }
        }
    }
}