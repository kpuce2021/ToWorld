package kr.ac.kpu.firstproject.ui

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_make_account.*
import kr.ac.kpu.firstproject.R

// sign up account
class MakeAccountActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_make_account)

        sign_in_button.setOnClickListener{
            when{
                TextUtils.isEmpty(sign_up_input_email.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@MakeAccountActivity,"이메일을 입력하시오",Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(sign_up_input_id.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@MakeAccountActivity, "아이디를 입력하시오", Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(sign_up_input_pswd.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@MakeAccountActivity, "비밀번호를 입력하시오", Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(sign_up_input_first_name.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@MakeAccountActivity, "이름을 입력하시오", Toast.LENGTH_SHORT).show()
                }
                TextUtils.isEmpty(sign_up_input_last_name.text.toString().trim() {it <= ' '}) -> {
                    Toast.makeText(this@MakeAccountActivity, "이름을 입력하시오", Toast.LENGTH_SHORT).show()
                }
                else -> {
                    val email = sign_up_input_email.text.toString().trim()
                    val password = sign_up_input_pswd.text.toString().trim()

                    FirebaseAuth.getInstance().createUserWithEmailAndPassword(email,password)
                        .addOnCompleteListener{ task ->
                            if(task.isSuccessful){
                                val firebaseUser = task.result!!.user!!

                                Toast.makeText(this@MakeAccountActivity,"인증 성공",Toast.LENGTH_SHORT).show()
                                val intent = Intent(this , MainActivity::class.java)
                                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK //새로운 Activity를 수행하고 현재 Activity를 스택에서 제거하기
                                intent.putExtra("user_id", firebaseUser.uid )
                                startActivity(intent)
                                finish()
                            }
                            else{
                                Toast.makeText(this@MakeAccountActivity,"인증 실패",Toast.LENGTH_SHORT).show()
                            }
                        }
                }
            }
        }
    }
}