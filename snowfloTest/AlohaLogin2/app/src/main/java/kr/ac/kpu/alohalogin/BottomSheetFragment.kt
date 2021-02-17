package kr.ac.kpu.alohalogin
import android.app.ProgressDialog
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.FirebaseStorage
import kotlinx.android.synthetic.main.bottomsheet_fragment.*
import java.io.File
import java.util.*

class BottomSheetFragment() : BottomSheetDialogFragment() {

    var userId: String = "noNamed"
    var userEmail: String = "noNamed"
    var fileName: String = "noNamed"

    private lateinit var database: DatabaseReference

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
        database.child(userId).child("fileName").setValue(fileName)
}

    fun uploadFile() {

        fileName = "record" + Random().nextInt(1000)

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




