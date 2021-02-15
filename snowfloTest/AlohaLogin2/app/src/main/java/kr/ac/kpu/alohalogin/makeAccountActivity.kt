package kr.ac.kpu.alohalogin

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import kotlinx.android.synthetic.main.activity_make_account.*

class  makeAccountActivity : AppCompatActivity() {

    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_make_account)


        sign_in_button.setOnClickListener{

            val email = sign_up_input_email.text.toString().trim()
            val password = sign_up_input_pswd.text.toString().trim() // trim(): 공백X

            print("email: "+ email+ "password: "+ password)
            Log.d("input_data","email: "+email+" password: "+password)
            // Toast.makeText(this,"email: "+ email+ "password: "+ password,Toast.LENGTH_SHORT).show() // debug1

            FirebaseAuth.getInstance().createUserWithEmailAndPassword(email,password)
                .addOnCompleteListener { task ->
                    if (task.isSuccessful) {

                        val user = auth.currentUser
                        Toast.makeText(this@makeAccountActivity,"인증 성공",Toast.LENGTH_SHORT).show()
                        // val intent = Intent(this@SplashActivity, ServiceActivity::class.java)
                        // COMMAND.clearActivityStack(intent)
                        // startActivity(intent)
                    } else {
                        Toast.makeText(this@makeAccountActivity,"인증 실패",Toast.LENGTH_SHORT).show()

                        // ToastMaker.getInstance().getHandler().sendEmptyMessage(2)
                        // goSignUp()
                    }
                }

        }
    }
}