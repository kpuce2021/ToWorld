package kr.ac.kpu.alohalogin
import android.app.ProgressDialog
import android.content.ContentValues.TAG
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.firebase.database.*
import com.google.firebase.database.ktx.database
import com.google.firebase.database.ktx.getValue
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.FirebaseStorage
import kotlinx.android.synthetic.main.bottomsheet_fragment.*
import java.io.File
import java.util.*

// send data firebase
class BottomSheetFragment() : BottomSheetDialogFragment() {

    var userId: String = "noNamed"
    var userEmail: String = "noNamed"
    var fileName: String = "noNamed"
    var fileNum: Int = 0 // file numbering

    private lateinit var database: DatabaseReference //firebase realtime DB 사용

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.bottomsheet_fragment, container, false)

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

        super.onViewCreated(view, savedInstanceState)

        select_button.setOnClickListener {

            userId = getArguments()?.getString("user_id").toString()
            userEmail = getArguments()?.getString("user_email").toString()
            /*
            userIdText.text=userId
            userEmailText.text=userEmail
            */
            // fileName = "너가 작성한 텍스트" + "uploadFile에 있는 fileName 지우기"
            checkName()
            checkNum()
            uploadFile()
            uploadData()
        }
    }

/*
    fun newInstance(isMyBoolean: Boolean) = BottomSheetFragment().apply {
        arguments = Bundle().apply {
            putBoolean("REPLACE WITH A STRING CONSTANT", isMyBoolean)
        }
    }
*/

    fun uploadData(){
        database = Firebase.database.reference
        database.child(userId).child("userId").setValue(userEmail)
        database.child(userId).child(fileName).child("number").setValue(fileNum) // "record" -> test를 위해 fileName
    }

    fun checkNum(){
        var tempString:String? = null
        database = Firebase.database.reference // realtimeDB reference 선언

        val realtimeDBEvent1 = object : ValueEventListener{
            override fun onDataChange(snapshot: DataSnapshot) {
                if(snapshot.child(userId).child(fileName).exists()){
                    tempString = snapshot.child(userId).child(fileName).child("number").getValue().toString()
                    fileNum = tempString!!.toInt() + 1
                }
                else{
                    fileNum = 0
                }
            }

            override fun onCancelled(error: DatabaseError) {
                Log.w(TAG, "loadPost:onCancelled", error.toException())
            }

        }
        database.addValueEventListener(realtimeDBEvent1)
    }

    fun checkName(){
        fileName = "discord" //
    }

    fun uploadFile() {
/*
        val realtimeDBEvent2 = object : ChildEventListener{
            override fun onChildAdded(snapshot: DataSnapshot, previousChildName: String?) { // 검색, 추가 대기
                if(snapshot.exists()){ 
                    
                }else{

                }
            }
            override fun onChildChanged(snapshot: DataSnapshot, previousChildName: String?) { // 변경 대기
                TODO("Not yet implemented")
            }

            override fun onChildRemoved(snapshot: DataSnapshot) { // 삭제 대기
                TODO("Not yet implemented")
            }

            override fun onChildMoved(snapshot: DataSnapshot, previousChildName: String?) { // 순서 변경 대기
                TODO("Not yet implemented")
            }

            override fun onCancelled(error: DatabaseError) {
                Log.w(TAG, "fileNumbers:onCancelled", error.toException())
                Toast.makeText(context, "Failed to load fileNumbers.",
                        Toast.LENGTH_SHORT).show()
            }
        }
*/

        // database.addChildEventListener(realtimeDBEvent2)
        // fileName = "record" + Random().nextInt(1000)
        // fileName = "discord"// fileName = record로 변경해야할듯

        var path:String = Environment.getExternalStorageDirectory().toString() + "/Download/myrec.3gp" //파일의 저장 위치
        val fileUri = Uri.fromFile(File(path))


        if(fileUri!=null){
            var pd = ProgressDialog(context)
            pd.setTitle("업로딩 중")
            pd.show()

            var mediaRef = FirebaseStorage.getInstance().reference.child(userEmail).child(fileName)
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




