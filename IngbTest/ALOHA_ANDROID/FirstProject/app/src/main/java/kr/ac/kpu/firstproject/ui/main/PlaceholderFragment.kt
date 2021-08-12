package kr.ac.kpu.firstproject.ui.main

import android.content.Intent
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.bumptech.glide.Glide
import kr.ac.kpu.firstproject.R

class PlaceholderFragment : Fragment() {

    private lateinit var pageViewModel: PageViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        /*
        Fragment가 살아있는 동안 ViewModelProvider를 생성
        생성이 완료되면 초기 Index 설정
         */
        pageViewModel = ViewModelProviders.of(this).get(PageViewModel::class.java).apply {
            setIndex(arguments?.getInt(ARG_SECTION_NUMBER) ?: 0)
        }
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val root =
            inflater.inflate(R.layout.fragment_walk_through, container, false) // Fragment View 이것이 프레그먼트를 연결시켜주는 거야

        val typedArray = context?.resources?.obtainTypedArray(R.array.walkthrough_images)

        val maintextView: TextView = root.findViewById(R.id.walk_through_main_text)
        pageViewModel.maintext.observe( viewLifecycleOwner, Observer<String> {
            maintextView.text = arguments?.getString(ARG_MAINTEXT)
        })

        val subtextView: TextView = root.findViewById(R.id.walk_through_sub_text)
        pageViewModel.maintext.observe( viewLifecycleOwner, Observer<String> {
            subtextView.text = arguments?.getString(ARG_SUBTEXT)
        })

        val imageView: ImageView = root.findViewById(R.id.walk_through_image)
        val button: Button = root.findViewById(R.id.walk_through_button)


        button.setOnClickListener {
            val nextIntent = Intent(context, kr.ac.kpu.firstproject.ui.MainActivity::class.java)
            startActivity(nextIntent)
            activity?.finish()
        }

        /*
        1. index가 변경될때마다 Image 변경
        2. index가 3일 때(0, 1, 2, 3) 버튼이 보이게 설정.
       */

        pageViewModel._index.observe( viewLifecycleOwner, Observer<Int> {
            val index = arguments?.getInt(ARG_SECTION_NUMBER) ?: 0
            if (typedArray != null) {
                Glide.with(this).load(typedArray.getResourceId(index, 0)).into(imageView)
            }

            if (index == 3) {
                button.visibility = View.VISIBLE
            } else {
                button.visibility = View.INVISIBLE
            }
        })

        return root
    }

    companion object{
        private const val ARG_SECTION_NUMBER = "section_number"
        private const val ARG_MAINTEXT = "maintext"
        private const val ARG_SUBTEXT = "subtext"


        //Fragment가 생성될 때 sectionNumber와 mainText와 subText를 받아오고 argument에 keyvalue 형식으로 값을 넣게 됨
        @JvmStatic
        fun newInstance(sectionNumber: Int, mainText: String, subText: String): PlaceholderFragment {
            return PlaceholderFragment().apply {
                arguments = Bundle().apply {
                    putInt(ARG_SECTION_NUMBER,sectionNumber)
                    putString(ARG_MAINTEXT, mainText)
                    putString(ARG_SUBTEXT, subText)
                }
            }
        }
    }
}