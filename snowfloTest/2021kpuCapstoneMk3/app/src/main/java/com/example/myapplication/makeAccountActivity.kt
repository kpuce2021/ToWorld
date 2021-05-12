package com.example.myapplication
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.util.Log
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.ktx.Firebase
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.ktx.database
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_make_account.*

// 회원가입
class  makeAccountActivity : AppCompatActivity() {

    private lateinit var auth: FirebaseAuth
    private lateinit var database: DatabaseReference //firebase realtime DB 사용

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_make_account)

        sign_in_button.setOnClickListener{
            when{
                TextUtils.isEmpty(sign_up_input_email.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@makeAccountActivity,"이메일을 입력하시오",Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(sign_up_input_id.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@makeAccountActivity, "아이디를 입력하시오", Toast.LENGTH_SHORT).show()

                }
                TextUtils.isEmpty(sign_up_input_pswd.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@makeAccountActivity, "비밀번호를 입력하시오", Toast.LENGTH_SHORT).show()

                }
                TextUtils.isEmpty(sign_up_input_first_name.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@makeAccountActivity, "이름을 입력하시오", Toast.LENGTH_SHORT).show()

                }
                TextUtils.isEmpty(sign_up_input_last_name.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@makeAccountActivity, "이름을 입력하시오", Toast.LENGTH_SHORT).show()

                }else -> {
                    var email = sign_up_input_email.text.toString().trim()
                    var password = sign_up_input_pswd.text.toString().trim()
                    // null error
                    Log.d("email",email)
                    Log.d("password",password)

                    FirebaseAuth.getInstance().createUserWithEmailAndPassword(email,password)
                        .addOnCompleteListener { task ->
                            if (task.isSuccessful) {

                                val firebaseUser = task.result!!.user!!

                                Toast.makeText(this@makeAccountActivity,"인증 성공",Toast.LENGTH_SHORT).show()
                                val intent = Intent(this , ServiceActivity::class.java)
                                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK //새로운 Activity를 수행하고 현재 Activity를 스택에서 제거하기
                                intent.putExtra("user_id", firebaseUser.uid )
                                startActivity(intent)
                                finish()

                            } else {
                                Toast.makeText(this@makeAccountActivity,"인증 실패",Toast.LENGTH_SHORT).show()

                                // ToastMaker.getInstance().getHandler().sendEmptyMessage(2)
                                // goSignUp()
                            }
                        }
                }
            }
        }
    }
    fun uploadAccount(userId:String){  // 가입하면 realtime DB에 추가
        database = Firebase.database.reference
        database.child(userId).setValue("userIdTest")
    }
}


