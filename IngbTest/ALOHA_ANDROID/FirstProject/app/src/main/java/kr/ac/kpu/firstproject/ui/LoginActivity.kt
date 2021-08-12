package kr.ac.kpu.firstproject.ui

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.view.animation.AnimationUtils
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_login.*
import kotlinx.android.synthetic.main.activity_main.*
import kr.ac.kpu.firstproject.R

// Main
class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val alertMessageAnim = AnimationUtils.loadAnimation(applicationContext, R.anim.alert_message_animation)

        login_button.setOnClickListener{
            when{
                TextUtils.isEmpty(input_email.text.toString().trim() { it <= ' ' }) -> {
                    Toast.makeText(this@LoginActivity,"이메일을 입력하시오",Toast.LENGTH_SHORT).show()
                }

                TextUtils.isEmpty(input_pswd.text.toString().trim() { it <= ' ' }) -> {
                    Toast.makeText(this@LoginActivity,"비밀번호를 입력하시오",Toast.LENGTH_SHORT).show()
                }
                else ->{
                    val email = input_email.text.toString().trim() { it <= ' ' }
                    val password = input_pswd.text.toString().trim() { it <= ' ' }

                    FirebaseAuth.getInstance().signInWithEmailAndPassword(email, password)
                        .addOnCompleteListener { task ->
                            if(task.isSuccessful){
                                val loginIntent = Intent(this, MainActivity::class.java)
                                loginIntent.flags =
                                    Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK //새로운 Activity를 수행하고 현재 Activity를 스택에서 제거하기
                                loginIntent.putExtra("user_email",input_email.text.toString())
                                startActivity(loginIntent)
                                finish()
                            }else{
                                alert_message.startAnimation(alertMessageAnim)
                            }
                        }
                }
            }
        }
        make_account_text.setOnClickListener {
            val intent = Intent(this, MakeAccountActivity::class.java)
            startActivity(intent)
        }
    }
}